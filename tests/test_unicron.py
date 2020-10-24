"""
Test Unicron application.

You may have to run reset.sh before this test. Note that will delete all test
logs.
"""
import datetime
import os
from pathlib import Path

# Ensure that main app var file references are in the test var directory, to
# keep the main one clean.
# NB. This must be done BEFORE unicron imports.
os.environ["TEST"] = "true"


from unicron.history import (
    get_last_run_date,
    check_need_to_run,
)
from unicron.logger import setup_logger
from unicron.run import run_in_shell
from unicron.paths import (
    mk_last_run_path,
    mk_output_path,
)


APP_DIR = Path("unicron")
VAR_DIR = APP_DIR / Path("_test_var")
LOG_DIR = VAR_DIR / "last_run"


def test_setup_logger():
    app_logger = setup_logger(__name__, VAR_DIR / "app.log", is_task=False)
    app_logger.debug("test_setup_logger", extra={"task": "pytest"})

    task_logger = setup_logger(__name__, LOG_DIR / "unit_task.log", is_task=True)
    task_logger.debug("test_setup_logger")


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


def test_get_last_run_date():
    assert get_last_run_date("never_run_before.sh") is None
    assert get_last_run_date("fail.sh") is None

    assert get_last_run_date("old.sh") == datetime.date(year=2020, month=1, day=1)
    assert get_last_run_date("today.sh") == datetime.date.today()


def test_check_need_to_run():
    # Expect to run.
    assert check_need_to_run("never_run_before.sh") is True
    assert check_need_to_run("fail.sh") is True
    assert check_need_to_run("old.sh") is True

    # Expect not to run.
    assert check_need_to_run("today.sh") is False
