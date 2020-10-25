"""
Run module tests.
"""
# pylint: disable=missing-function-docstring
from unicron import run


def test_run_in_shell_success():
    cmd = 'echo "Test output"'
    success, output = run.run_in_shell(cmd)

    assert success
    assert output == "Test output"


def test_run_in_shell_fail():
    cmd = "echo Fail! ; exit 1"
    success, output = run.run_in_shell(cmd)

    assert not success
    assert output == "Fail!"
