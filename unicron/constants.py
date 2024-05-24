"""
Constants module.
"""

import os
from pathlib import Path


USE_TEST_MODE = os.environ.get("TEST") is not None

APP_DIR = Path(__file__).resolve().parent
VAR_DIR = APP_DIR / ("_test_var" if USE_TEST_MODE else "var")

TASKS_DIR = VAR_DIR / "targets"
LAST_RUN_DIR = VAR_DIR / "last_run"
RUN_EXT = ".txt"

APP_LOG_PATH = VAR_DIR / "app.log"
OUTPUT_DIR = VAR_DIR / "output"
OUTPUT_EXT = ".log"
