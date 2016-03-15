import click
import json
import os
import sys

from shakedown.cli.helpers import *


@click.command('shakedown')
@click.argument('path', type=click.Path(exists=True), nargs=-1)
@click.option('--dcos_url', help='URL to a running DCOS cluster.')
@click.option('--fail', type=click.Choice(['fast', 'never']), default='fast', help='Sepcify whether to continue testing when encountering failures. (default: fast)')
@click.option('--ssh_key_file', type=click.Path(), help='Path to the SSH keyfile to use for authentication')
@click.option('--no_banner', is_flag=True, help='Suppress the product banner.')
@click.option('--quiet', is_flag=True, help='Suppress all superfluous output.')
@click.option('--report', type=click.Choice(['json', 'junit']), help='Return a report in the specified format.')
@click.option('--stdout', type=click.Choice(['pass', 'fail', 'skip', 'all', 'none']), default='fail', help='Print the standard output of tests with the specified result. (default: fail)')
@click.version_option(version=shakedown.VERSION)


def cli(**args):
    """ Main CLI entry-point; perform pre-flight and parse arguments
    """
    import shakedown as shakedown

    if args['quiet']:
        shakedown.cli.quiet = True

    if args['dcos_url']:
        os.environ["TEST_MASTER_URI"] = args['dcos_url']
    else:
        click.secho('error: --dcos_url is a required option; see --help for more information.', fg='red', bold=True)
        exit(1)

    if args['ssh_key_file']:
        shakedown.cli.ssh_key_file = os.path.expanduser(args['ssh_key_file'])

    if not args['no_banner']:
        echo(banner(), n=False)

    echo('Running pre-flight checks...', d='step-maj')
    echo('Checking for pytest library...', d='step-min', n=False)
    try:
        import pytest
    except ImportError:
        click.secho("error: pytest is not installed; run 'pip install pytest'.", fg='red', bold=True)
        exit(1)
    echo(pytest.__version__)
    echo('Checking for dcos library...', d='step-min', n=False)
    try:
        import dcos
    except ImportError:
        click.secho("error: dcos is not installed; run 'pip install dcos'.", fg='red', bold=True)
        exit(1)
    echo(dcos.version)
    echo('Checking DCOS cluster state...', d='step-min', n=False)
    try:
        from dcos import (config, marathon, util)

        with stdchannel_redirected(sys.stdout, os.devnull):
            config.set_val('core.dcos_url', args['dcos_url'])

        with stdchannel_redirected(sys.stderr, os.devnull):
            dcos_config = util.get_config()
            init_client = marathon.create_client(dcos_config)
    except:
        click.secho("error: cluster '" + args['dcos_url'] + "' is unreachable.", fg='red', bold=True)
        exit(1)
    echo('running')


    class shakedown:
        """ This encapsulates a PyTest wrapper plugin
        """

        state = {}

        tests = {
            'file': {},
            'test': {}
        }

        report_stats = {
            'passed':[],
            'skipped':[],
            'failed':[],
            'total_passed':0,
            'total_skipped':0,
            'total_failed':0,
        }


        def pytest_collectreport(self, report):
            """ Collect and validate individual test files
            """

            if not 'collect' in shakedown.state:
                shakedown.state['collect'] = 1
                echo('Collecting and validating test files...', d='step-min')

            if report.nodeid:
                echo(report.nodeid, d='item-maj', n=False)

                if report.failed:
                    echo('import fail', d='fail')
                else:
                    echo(chr(10003), d='pass')

                if args['stdout'] and report.longrepr:
                    state = None

                    if report.failed and args['stdout'] in ['fail', 'all']:
                        state = 'fail'
                    if report.passed and args['stdout'] in ['pass', 'all']:
                        state = 'pass'
                    if report.skipped and args['stdout'] in ['skip', 'all']:
                        state = 'skip'

                    if state:
                        try:
                            shakedown.tests['test'][report.nodeid]
                        except KeyError:
                            shakedown.tests['test'][report.nodeid] = {}

                        shakedown.tests['test'][report.nodeid][state] = str(report.longrepr).rstrip()


        def pytest_sessionstart(self):
            """ Tests have been collected, begin running them...
            """

            echo('Initiating testing phase...', d='step-maj')


        def pytest_report_teststatus(self, report):
            """ Print report results to the console as they are run
            """

            try:
                report_file, report_test = report.nodeid.split('::', 1)
            except ValueError:
                return

            if not 'test' in shakedown.state:
                shakedown.state['test'] = 1
                echo('Running individual tests...', d='step-min')

            if not report_file in shakedown.tests['file']:
                shakedown.tests['file'][report_file] = 1
                echo(report_file, d='item-maj')
            if not report.nodeid in shakedown.tests['test']:
                shakedown.tests['test'][report.nodeid] = {}
                echo(report_test, d='item-min', n=False)

            if report.passed:
                echo(report.when, d='pass', n=False)
            elif report.skipped:
                echo(report.when, d='skip', n=False)
            elif report.failed:
                echo(report.when, d='fail', n=False)

            if report.when == 'teardown':
                echo('')

            # Suppress excess terminal output
            return report.outcome, None, None


        def pytest_runtest_logreport(self, report):
            """ Log the [stdout, stderr] results of tests if desired
            """

            if args['stdout']:
                state = None

                for secname, content in report.sections:
                    if report.failed and args['stdout'] in ['fail', 'all']:
                        state = 'fail'
                    if (report.passed) and args['stdout'] in ['pass', 'all']:
                        state = 'pass'
                    if report.skipped and args['stdout'] in ['skip', 'all']:
                        state = 'skip'

                    if state and report.when == 'call':
                        if not state in shakedown.tests['test'][report.nodeid]:
                            shakedown.tests['test'][report.nodeid][state] = content
                        else:
                            shakedown.tests['test'][report.nodeid][state] += content


        def pytest_runtest_makereport(self, item, call, __multicall__):
            """ Store "simple" (pass, fail, skip) test results
            """

            report = __multicall__.execute()

            # Put job run report data into shakedown.report_status hash
            if report.passed:
                shakedown.report_stats['passed'].append(report.nodeid + '.' + report.when)
                shakedown.report_stats['total_passed'] += 1
            if report.failed:
                shakedown.report_stats['failed'].append(report.nodeid + '.' + report.when)
                shakedown.report_stats['total_failed'] += 1
            if report.skipped:
                shakedown.report_stats['skipped'].append(report.nodeid + '.' + report.when)
                shakedown.report_stats['total_skipped'] += 1

            return report


        def pytest_sessionfinish(self, session, exitstatus):
            """ Testing phase is complete; print extra reports (stdout/stderr, JSON) as requested
            """

            echo('Test phase completed.', d='step-maj')

            if ('stdout' in args and args['stdout']) and \
                    ('test' in shakedown.tests and shakedown.tests['test']):
                for test in sorted(shakedown.tests['test']):
                    for result in ['fail', 'pass', 'skip']:
                        if result in shakedown.tests['test'][test]:
                            echo('Output during ', d='quote-head-' + result, n=False)

                            shakedown.tests['test'][test][result] = shakedown.tests['test'][test][result].strip()

                            if 'quiet' in args and args['quiet']:
                                print('-' * len(test) + "\n" + test + "\n" + '-' * len(test))
                                print(shakedown.tests['test'][test][result])
                            else:
                                click.secho(decorate(test, style=result), bold=True)
                                click.echo(decorate(shakedown.tests['test'][test][result], style='quote-' + result))

            if args['report'] == 'json':
                click.echo("\n" + json.dumps(shakedown.report_stats, sort_keys=True, indent=4, separators=(',', ': ')))

    opts = ['-q', '--tb=no']

    if args['fail'] == 'fast':
        opts.append('-x')

    if args['path']:
        opts.append(' '.join(args['path']))

    pytest.main(' '.join(opts), plugins=[shakedown()])
