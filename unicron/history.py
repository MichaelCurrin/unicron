"""
History module.

Check when a task last ran and if it needs to run today.
"""
import datetime

from . import constants, logger, paths


def get_last_run_date(task_name: str):
    """
    Get date of a task's last run file and return as a qdatetime object if set.
    """
    last_run_path = paths.mk_last_run_path(task_name)

    if last_run_path.exists():
        last_run = last_run_path.read_text().strip()
        if last_run:
            return datetime.datetime.strptime(last_run, "%Y-%m-%d").date()

    return None


def check_need_to_run(task_name: str) -> bool:
    """
    Check whether the given task needs to run today.

    If a last run file exists for the task, the file is non-empty and contains
    a valid YYYY-MM-DD date which matches today's date, then the task can be
    skipped. Otherwise it needs to be run today.

    The debug-level messages here are useful for in development for checking
    on the reason for executing, but otherwise they can be ignored.
    """
    app_logger = logger.setup_logger("unicron", constants.APP_LOG_PATH)
    extra = {"task": task_name}

    last_run_date = get_last_run_date(task_name)

    if last_run_date:
        if last_run_date == datetime.date.today():
            app_logger.info("Skipping, since already ran today.", extra=extra)
            status = False
        else:
            app_logger.debug("Executing, since last run date is old.", extra=extra)
            status = True
    else:
        app_logger.debug("Executing, since no run record found.", extra=extra)
        status = True

    return status
