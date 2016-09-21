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
