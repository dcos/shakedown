from click.testing import CliRunner

from shakedown import *


def test_cli_require_dcos_uri():
    runner = CliRunner()
    result = runner.invoke(cli.main.cli)
    assert result.exit_code == 1

def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli.main.cli, ['--version'])
    assert result.exit_code == 0
    assert result.output == "shakedown, version " + shakedown.VERSION + "\n"

