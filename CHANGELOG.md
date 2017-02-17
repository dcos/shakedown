## 1.2.0 (2017-02-17)

Features:

  - ability to skip tests based on required resources, DC/OS versioning
    - eg. `@pytest.mark.skipif('required_cpus(2)')` and `@dcos_1_9`
  - support for deleting leftover data following persistent service
    uninstall (ie.a `janitor.py` shim)
      - `delete_persistent_data()`
      - `destroy_volume()` / `destroy_volumes()`
      - `unreserve_resources()` / `unreserve_resources()`
  - command methods now allow disabling output and/or raising on error
  - marathon methods add `delete_app`/`delete_app_wait` for a specific app
  - package install methods support waiting for service tasks to start
    running, additional logging
  - package uninstall methods add support for deleting persistent volumes
    after uninstall
  - packge repo methods support waiting for add/remove repo to complete,
    check for a changed package version
  - service method function for deleting persistent volumes
  - service method support waiting for task rollout to complete
  - service method verifying that tasks are not changed

Fixes:

  - marathon methods fix unused `app_id` when checking deployment
  - `hello-world` package (previously `riak`) now used to test
    `test_install_package_with_subcommand()`
  - spinner-related fixes:
    - while a spinner is polling, print the spin time and any
      ignored exceptions by default
    - don't drop the original stack when rethrowing exceptions
    - return the result of the spin at the end of `wait_for`,
      allowing passthrough of the predicate return value

## 1.1.15 (2017-02-03)

Features:

  - split `requirements.txt` and `requirements-edge.txt` for
    building against `dcoscli:master`

Fixes:

  - `_wait()` functions now wait on deployment, not health
  - uninstalls now wait for Mesos task removal
  - tests fixed for package installation and waiting
  - improved error messaging when unable to connect to a host

## 1.1.14 (2017-01-13)

Features:

  - new cluster functions `get_resources`, `resources_needed`,
    `get_used_resources`, `get_unreserved_resources`,
    `get_reserved_resources`, and `available_resources`

## 1.1.13 (2017-01-05)

Features:

  - bumped `dcosdcli` version to `0.4.15`

Fixes:

  - `timeout_sec` passed through to `time_wait()` method

## 1.1.12 (2016-12-27)

Features:

  - SSH user (default `core`) can be specified on the command line
    with `--ssh-user`
  - new ZooKeeper `get_zk_node_data` function`

Fixes:

  - `test_install_package_with_json_options` test is set to `xfail`
    while it is being diagnosed

## 1.1.11 (2016-12-13)

Features:

  - test timeouts as defined by `--timeout` (or `timeout` in
    `.shakedown` config) or `@pytest.mark.timeout(n)` for
    individual tests

Fixes:

  - exit code is now returned for `run_dcos_command` calls
  - fallbaack to `ssh-agent` if `.ssh/id_rsa` key fails
  - `wait` predicate fixed from `1.1.9`
  - use `service_name` rather than former ambiguous `app_id`

## 1.1.10 (2016-11-08)

Fixes:

  - fixing broken PyPI 1.1.9 release

## 1.1.9 (2016-11-08)

Features:

  - 'wait' functions and predicates, including `wait_for_task`,
    `wait_for_task_property`, `wait_for_dns`, and `deployment_wait`
  - new marathon methods for `deployment_wait`, `delete_all_apps`,
    and `delete_all_apps_wait`
  - support for passing a dict object containing JSON options to
    `install_package` methods
  - bumped `dcosdcli` version to `0.4.14`

Fixes:

  - pep8-compliance

## 1.1.8 (2016-11-01)

Features:

  - `--dcos-url` now defaults to pre-configured dcos-cli value
  - `dcos_dns_lookup` method for resolving Mesos-DNS queries
  - reworked network paritioning methods, including new utility
    methods for `disconnected_agent`, `disconnected_master`,
    `save_iptables`, `flush_all_rules`, `allow_all_traffic`, and
    `iptable_rules`
  - added `tox.ini` configuration file

Fixes:

  - fixed documentation for `get_private_agents()`

## 1.1.7 (2016-10-20)

Features:

  - `--fail` now defaults to `never`
  - the `run_command` and associated agent/master methods now return
    both the exit status and captured output

Fixes:

  - `kill_process_on_host` method now working, better output
  - improved `--stdout-inline` readability
  - fixed bug where output from teardown methods did not display if
    module only had a single test

## 1.1.6 (2016-10-14)

Features:

  - `--username`, `--password`, and `--oauth-token` can now be
    specified via the command line
  - updated documentation on installing via PyPI or with virtualenv

Fixes:

  - authentication methods (OAuth, user/pass) are only attempted
    when the related options are defined
  - removed `pytest_runtest_makereport` method which was unused and
    causing pytest warning messages on every run

## 1.1.5 (2016-10-12)

Fixes:

  - cluster authentication attempts are sequenced (existing ACS token ->
    OAuth token -> username/password combo)
  - output from module setup and teardown is now printed to stdout
  - multiple test files (or multiple tests) can be again be specified
    (broken in `1.1.4`)


## 1.1.4 (2016-10-07)

Features:

  - allow a session to be authenticated using a supplied OAuth token
    in `.shakedown` (`oauth_token = <token>`)
  - new `delete_agent_log` method to delete logs on agents
  - pytest-style single-test specification (`test_file.py::test_name`)

Fixes:

  - `dcos-shakedown` command now functions correctly from cmd


## 1.1.3 (2016-10-04)

Features:

  - bumped `dcosdcli` version to `0.4.13`
  - modified CLI 'short' flags to match SSH/curl

Fixes:

  - removed superfluous `key not found` error message when SSH
    key could not be located


## 1.1.2 (2016-09-21)

Features:

  - new `--pytest-option` flag to pass CLI options on to pytest
  - short (single-character) flags for commonly-used CLI options

Fixes:

  - improved `--help` CLI output


## 1.1.1 (2016-09-20)

Initial implementation of changelog.

Features:

  - new `partition_master` and `reconnect_master` methods

Fixes:

  - added missing API documentation for `authenticate` method
  - updated PyPI packaging name to `dcos-shakedown`
  - renamed `task_name` to `task_id` in task methods
  - check the exit code of the command in `run_command` method`
