#!/usr/bin/env python3
"""
Unicron main application file.

Purpose:

Check for configured tasks and run them if needed. If this main script is run
multiple times in a day, it will still only execute each script once, or as
many times as it takes to get a success.

Checking and running:

Iterate through files in the configured targets directory. These should all be
executables. If there is a record that says the executable has not run today,
then run it and on success then add record that it ran today. If the script
fails, leave the record as it was.

Printing and logging:

Whether any task need are attempted to run or not, nothing will print to the
console unless there are any errors running a task. This allows the crontab run
messages to be quiet. For manual testing, use the --verbose flag to see
everything the main app does.

The app always logs the same number messages to the app log file, regardless of
verbosity level. Output of tasks is always logged to each tasks output file,
using info or error level depending on task success or failure.

Dev notes:

Regarding APP_DIR - make sure to resolve to absolute path first, so it works if
we an symlink to this without getting the parent directory of the symlink. This
problem would  not apparent when running the script directly without using a
symlink.
"""
import argparse
import datetime
import logging
import subprocess
import os
import sys
import textwrap
from pathlib import Path
from typing import List, Tuple


USE_TEST_MODE = os.environ.get("TEST") is not None

APP_DIR = Path(__file__).resolve().parent
VAR_DIR = APP_DIR / ("_test_var" if USE_TEST_MODE else "var")

TASKS_DIR = VAR_DIR / "targets"
LAST_RUN_DIR = VAR_DIR / "last_run"
RUN_EXT = ".txt"

APP_LOG_PATH = VAR_DIR / "app.log"
OUTPUT_DIR = VAR_DIR / "output"
OUTPUT_EXT = ".log"

APP_FORMATTER = logging.Formatter(
    "%(asctime)s %(levelname)s:%(filename)s %(task)s - %(message)s"
)
TASK_FORMATTER = logging.Formatter(
    "%(asctime)s %(levelname)s:%(filename)s - %(message)s"
)

VERBOSE = None


def setup_logger(name: str, log_file: Path, is_task: bool = False):
    """
    Configure a logger object and return it.

    It is safer to run this setup multiple in a script as the log file handler
    will only be added if it not there already.

    >>> app_logger = setup_logger('foo', 'foo.log')
    >>> app_logger.info('This is just an info message.')

    >>> task_logger = setup_logger('bar', 'bar.log', is_task=True)
    >>> task_logger.info('This is just an info message.')
    """
    formatter = TASK_FORMATTER if is_task else APP_FORMATTER

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        if not is_task:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            stream_lvl = logging.DEBUG if VERBOSE else logging.ERROR
            stream_handler.setLevel(stream_lvl)
            logger.addHandler(stream_handler)

    return logger


def run_in_shell(cmd: str) -> Tuple[bool, str]:
    """
    Run given command in the shell and return result of the command.

    Usually a malformed command or error in the executed code will result in
    the CalledProcessError and then that message is shown. During development
    of this project, the OSError was experienced so this is covered below too.

    :return success: True if ran without error, False otherwise.
    :return output: Text result of the command. If there was an error, this
        will be the error message.
    """
    try:
        exitcode, output = subprocess.getstatusoutput(cmd)
    except OSError as os_err:
        success = False
        output = str(os_err)
    else:
        success = exitcode == 0

    return success, output


def mk_last_run_path(task_name: str) -> Path:
    """
    Return full path to a task's last run file.
    """
    return LAST_RUN_DIR / "".join((task_name, RUN_EXT))


def mk_output_path(task_name: str) -> Path:
    """
    Return output file path for a task.
    """
    return OUTPUT_DIR / "".join((task_name, OUTPUT_EXT))


def get_last_run_date(task_name: str):
    """
    Get data of task's last run file and return as datetime object if set.
    """
    last_run_path = mk_last_run_path(task_name)

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
    app_logger = setup_logger("unicron", APP_LOG_PATH)
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


def proccess_cmd_result(
    task_name: str, task_log_path: Path, last_run_path: Path, status: bool, output: str
) -> None:
    """
    Process the result of running a command.

    Log activity for the task and update the last run date if the task was
    successful.
    """
    assert status is not None, "Status must indicate success (True) or fail (False)."

    app_logger = setup_logger("unicron", APP_LOG_PATH)
    task_logger = setup_logger(task_name, task_log_path, is_task=True)

    extra = {"task": task_name}
    output_log_msg = f"Output:\n{textwrap.indent(output, ' '*4)}"

    if status:
        app_logger.info("Success.", extra=extra)
        task_logger.info(output_log_msg)

        today = datetime.date.today()
        last_run_path.write_text(str(today))
    else:
        app_logger.error(
            "Task exited with error status! Check this task's log: %s",
            task_log_path,
            extra=extra,
        )
        task_logger.error(output_log_msg)


def execute(task_name: str) -> bool:
    """
    On a succesful run, set today's date in the last run event file for the
    executable, so that on subsequent runs today this executable will be
    ignored. On a failing run, do not update the file so we leave it marked as
    need to run today still.

    Regardless of the executed task's output, capture all output and send it to
    a log file dedicated to that task. This makes it easy to view the
    executable's history later.

    :return status: True if ran without error, False otherwise.
    """
    last_run_path = mk_last_run_path(task_name)

    task_log_path = mk_output_path(task_name)
    task_logger = setup_logger(task_name, task_log_path, is_task=True)

    task_logger.info("Executing...")
    cmd = TASKS_DIR / task_name
    status, output = run_in_shell(str(cmd))

    proccess_cmd_result(task_name, task_log_path, last_run_path, status, output)

    return status


def handle_task(task_name):
    """
    Run a task, if it needs to run now.

    :return status: True on task success, False on failure and None on not
        running.
    """
    should_run = check_need_to_run(task_name)

    if should_run:
        status = execute(task_name)
    else:
        status = None

    return status


def get_tasks() -> List[str]:
    """
    Get Path objects for tasks in the configured tasks diectory.
    """
    globbed_tasks = sorted(TASKS_DIR.iterdir())

    return [p.name for p in globbed_tasks if not p.name.startswith(".")]


def handle_tasks() -> Tuple[int, int, int]:
    """
    Find tasks, check their run status for today and run any if needed.

    :return: tuple of results.
    """
    success = fail = skipped = 0

    app_logger = setup_logger("unicron", APP_LOG_PATH, is_task=False)
    extra = {"task": "unicron"}

    tasks = get_tasks()
    msg = f"Task count: {len(tasks)}"
    app_logger.info(msg, extra=extra)

    for task_name in tasks:
        status = handle_task(task_name)

        if status is True:
            success += 1
        elif status is False:
            fail += 1
        else:
            skipped += 1

    msg = f"Succeeded: {success}; Failed: {fail}; Skipped: {skipped}"
    app_logger.info(msg, extra=extra)

    return success, fail, skipped


def main() -> None:
    """
    Main command-line argument parser.

    :raises: Exit script on error code if there are any failures.
    """
    global VERBOSE  # pylint: disable=global-statement

    parser = argparse.ArgumentParser(
        description="Uniron task scheduler.",
        epilog="Run against the test var directory, using TEST=1 as script prefix.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        help="If supplied print all app log messages to the console and not"
        " just errors and higher",
        action="store_true",
    )
    args = parser.parse_args()
    if args.verbose:
        VERBOSE = True

    _, fail, _ = handle_tasks()

    if fail != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
