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
import sys
from typing import List, Tuple

from . import constants, history, logger, run


def handle_task(task_name):
    """
    Run a task, if it needs to run now.

    :return status: True on task success, False on failure and None on not
        running.
    """
    should_run = history.check_need_to_run(task_name)

    if should_run:
        status = run.execute(task_name)
    else:
        status = None

    return status


def get_tasks() -> List[str]:
    """
    Get Path objects for tasks in the configured tasks diectory.
    """
    globbed_tasks = sorted(constants.TASKS_DIR.iterdir())

    return [p.name for p in globbed_tasks if not p.name.startswith(".")]


def handle_tasks() -> Tuple[int, int, int]:
    """
    Find tasks, check their run status for today and run any if needed.

    :return: tuple of results.
    """
    success = fail = skipped = 0

    app_logger = logger.setup_logger("unicron", constants.APP_LOG_PATH, is_task=False)
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
    logger.VERBOSE = args.verbose

    _, fail, _ = handle_tasks()

    if fail != 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
