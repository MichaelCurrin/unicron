#!/usr/bin/env python
"""
Uni-Cron main application file.

Check for configured tasks and run them if needed.  If this main script is run
multiple times in a day, it will still only execute each script once, or as
many times as it takes to get a success.

How it works:
    Iterate through files in the configured targets directory. These should all
    be executables. If there is a record that says the executable has not run
    today, then run it and on success then add record that it ran today. If the
    script fails, leave the record as it was.
"""
import argparse
import datetime
import logging
import subprocess
import os
import textwrap
from pathlib import Path


USE_TEST_MODE = os.environ.get('TEST') is not None

APP_DIR = Path(__file__).parent.resolve()
VAR_DIR = APP_DIR / ('_test_var' if USE_TEST_MODE else 'var')

TASKS_DIR = VAR_DIR / 'targets'
LAST_RUN_DIR = VAR_DIR / 'last_run'
RUN_EXT = '.txt'

APP_LOG_PATH = VAR_DIR / 'app.log'
OUTPUT_DIR = VAR_DIR / 'output'
OUTPUT_EXT = '.log'

APP_FORMATTER = logging.Formatter(
    '%(asctime)s %(levelname)s:%(filename)s %(task)s - %(message)s')
TASK_FORMATTER = logging.Formatter(
    '%(asctime)s %(levelname)s:%(filename)s - %(message)s')
app_logger = None


def setup_logger(name, log_file, is_task=False):
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

    return logger


app_logger = setup_logger('unicron', APP_LOG_PATH)


def run_in_shell(cmd: str):
    """
    Run given command in the shell.
    """
    cmd_list = [cmd]

    try:
        result = subprocess.check_output(
            cmd_list,
            stderr=subprocess.STDOUT,
            shell=True
        )
    except subprocess.CalledProcessError as e:
        success = False
        output = e.output.decode()
    except OSError as e:
        success = False
        output = str(e)
    else:
        success = True
        output = result.decode()

    return success, output


def execute(task_name, last_run_path, extra):
    """
    On a succesful run, set today's date in the last run event file for the
    executable, so that on subsequent runs today this executable will be
    ignored. On a failing run, do not update the file so we leave it marked as
    need to run today still.

    Regardless of the executed task's output, capture all output and send it to
    a log file dedicated to that task. This makes it easy to view the
    executable's history later.

    :return: None
    """
    task_log_path = OUTPUT_DIR / "".join((task_name, OUTPUT_EXT))
    task_logger = setup_logger(task_name, task_log_path, is_task=True)

    task_logger.info("Executing...")
    cmd = TASKS_DIR / task_name
    success, output = run_in_shell(cmd)

    output_log_msg = f"Output:\n{textwrap.indent(output, ' '*4)}"
    if success:
        app_logger.info("Success.", extra=extra)
        task_logger.info(output_log_msg)
        today = datetime.date.today()
        last_run_path.write_text(today.strftime('%Y%m%d'))
    else:
        app_logger.error(
            "Exited with error status! Check this task's log.", extra=extra)
        task_logger.error(output_log_msg)


def handle_tasks():
    """
    Find tasks, check their run status for today and run any if needed.

    :return: None
    """
    today = datetime.date.today()

    globbed_tasks = sorted(TASKS_DIR.iterdir())
    tasks = [p.name for p in globbed_tasks if not p.name.startswith('.')]

    for task_name in tasks:
        extra = {'task': task_name}

        last_run_path = LAST_RUN_DIR / "".join((task_name, RUN_EXT))

        if last_run_path.exists():
            last_run = last_run_path.read_text().strip()
            last_run_date = datetime.datetime.strptime(
                last_run, '%Y%m%d').date()
        else:
            last_run_date = None

        if not last_run_date:
            app_logger.debug(
                "Executing, since no run record.", extra=extra)
        elif last_run_date != today:
            app_logger.debug(
                "Executing, since date is old.", extra=extra)
        else:
            app_logger.info("Skipping, since already ran today.", extra=extra)
            continue

        execute(task_name, last_run_path, extra)


def main():
    """
    Main command-line argument parser.

    :return: None
    """
    parser = argparse.ArgumentParser(description="Uni-Cron task scheduler.")
    args = parser.parse_args()

    handle_tasks()


if __name__ == '__main__':
    main()
