"""
Test Unicron application.

You may have to run reset.sh before this test. Note that will delete all test
logs.
"""
import os
from pathlib import Path

# Ensure that main app var file references are in the test var directory, to
# keep the main one clean. This must be done before unicron imports.
os.environ["TEST"] = "true"

from unicron.unicron import setup_logger, run_in_shell, mk_last_run_path, mk_output_path


APP_DIR = Path("unicron")
VAR_DIR = APP_DIR / Path("_test_var")
LOG_DIR = VAR_DIR / "last_run"


def test_setup_logger():
    app_logger = setup_logger(__name__, VAR_DIR / "app.log", is_task=False)
    task_logger = setup_logger(__name__, LOG_DIR / "unit_task.log", is_task=True)


def test_run_in_shell_success():
    cmd = 'echo "Test output"'
    success, output = run_in_shell(cmd)
    assert success
    assert output == "Test output"


def test_run_in_shell_fail():
    cmd = "echo Fail! ; exit 1"
    success, output = run_in_shell(cmd)
    assert not success
    assert output == "Fail!"


def test_mk_last_run_path():
    path = mk_last_run_path("foo")
    assert str(path).endswith("_test_var/last_run/foo.txt")


def test_mk_output_path():
    path = mk_output_path("foo")
    assert str(path).endswith("_test_var/output/foo.log")
