"""
Paths module.
"""

from pathlib import Path

from . import constants


def mk_last_run_path(task_name: str) -> Path:
    """
    Return full path to a task's last run file.
    """
    return constants.LAST_RUN_DIR / "".join((task_name, constants.RUN_EXT))


def mk_output_path(task_name: str) -> Path:
    """
    Return output file path for a task.
    """
    return constants.OUTPUT_DIR / "".join((task_name, constants.OUTPUT_EXT))
