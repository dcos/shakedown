from click.testing import CliRunner

import shakedown

from shakedown.cli.main import cli


def test_cli_require_dcos_uri():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 1

def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert result.output == "shakedown, version " + shakedown.VERSION + "\n"

