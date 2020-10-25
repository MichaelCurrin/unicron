"""
Logger module tests.
"""
# pylint: disable=missing-function-docstring
from pathlib import Path

from unicron import logger


APP_DIR = Path("unicron")
VAR_DIR = APP_DIR / Path("_test_var")
LOG_DIR = VAR_DIR / "last_run"


def test_setup_logger():
    app_logger = logger.setup_logger(__name__, VAR_DIR / "app.log", is_task=False)
    app_logger.debug("test_setup_logger", extra={"task": "pytest"})

    task_logger = logger.setup_logger(__name__, LOG_DIR / "unit_task.log", is_task=True)
    task_logger.debug("test_setup_logger")
