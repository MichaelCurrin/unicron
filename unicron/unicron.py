#!/usr/bin/env python
"""
Uni-Cron main application file.

Check for configured tasks and run them if needed.
"""
import argparse
import datetime
import logging
import subprocess
from pathlib import Path


APP_DIR = Path(__file__).parent.resolve()

# TODO: Check for env variable or flags.
if True:
    VAR_DIR = APP_DIR / '_test_var'
else:
    VAR_DIR = APP_DIR / 'var'

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


def setup_logger(name, log_file, is_task=False):
    """
    Allow easy creation of multiple loggers.

    Write to a log file. In some cases, also print to the console, which is useful when debugging by hand.

    >>> app_logger = setup_logger('foo', 'foo.log')
    >>> app_logger.info('This is just an info message.')

    >>> task_logger = setup_logger('bar', 'bar.log', is_task=True)
    >>> app_logger.info('This is just an info message.')
    """
    formatter = TASK_FORMATTER if is_task else APP_FORMATTER

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def execute(task_name, last_run_path):
    """
    On a succesful run, set today's date in the last run event file for the
    executable, so that on subsequent runs today this executable will be
    ignored. On a failing run, do not update the file so we leave it marked as
    need to run today still.

    Regardless of the executed task's output, capture all output and send it to
    a log file dedicated to that task. This makes it easy to view the
    executable's history later.
    """
    cmd = TASKS_DIR / task_name
    output_path = OUTPUT_DIR / "".join((task_name, OUTPUT_EXT))

    task_log_path = OUTPUT_DIR / "".join((task_name, OUTPUT_EXT))
    task_logger = setup_logger(task_name, task_log_path, is_task=True)
    task_logger.info("Executing...")


def handle_tasks():
    """
    Find tasks, check their run status for today and run any if needed.
    """
    today = datetime.date.today()

    tasks = [p.name for p in TASKS_DIR.iterdir() if not p.name.startswith('.')]

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

        execute(task_name, last_run_path)


app_logger = setup_logger('unicron', APP_LOG_PATH)


def main():
    """
    Main command-line argument parser.
    """
    parser = argparse.ArgumentParser(description="Uni-Cron task scheduler.")
    args = parser.parse_args()

    handle_tasks()


if __name__ == '__main__':
    main()
