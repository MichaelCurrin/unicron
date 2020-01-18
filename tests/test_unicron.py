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

from unicron.unicron import setup_logger


APP_DIR = Path("unicron")
VAR_DIR = APP_DIR / Path("_test_var")
LOG_DIR = VAR_DIR / "last_run"


def test_setup_logger():
    app_logger = setup_logger(__name__, VAR_DIR / "app.log", is_task=False)
    task_logger = setup_logger(__name__, LOG_DIR / "unit_task.log", is_task=True)
