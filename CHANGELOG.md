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
