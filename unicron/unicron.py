#!/usr/bin/env python
"""
Uni-Cron application entry point.
"""
import argparse
import datetime
import logging
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
    '%(asctime)s %(levelname)s:%(name)s %(task)s - %(message)s')
TASK_FORMATTER = logging.Formatter(
    '%(asctime)s %(levelname)s:%(name)s - %(message)s')


def setup_logger(name, log_file, is_task=False):
    """
    Allow easy creation of multiple loggers.

    >>> app_logger = setup_logger('foo', 'foo.log')
    >>> app_logger.info('This is just an info message.')

    >>> task_logger = setup_logger('bar', 'bar.log', is_task=True)
    >>> app_logger.info('This is just an info message.')
    """
    level = logging.DEBUG

    handler = logging.FileHandler(log_file)
    formatter = TASK_FORMATTER if is_task else APP_FORMATTER
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def handle_tasks():
    """
    Find tasks, check their run status for today and run any if needed.
    """
    today = datetime.date.today()
    app_logger = setup_logger('unicron', APP_LOG_PATH)
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
                "Executing, since run file is missing.", extra=extra)
            continue

        if last_run_date == today:
            app_logger.info("Skipping, since already ran today.", extra=extra)
        else:
            app_logger.debug(
                "Executing, since run file's date is old.", extra=extra)

        app_logger.info("Executing", extra=extra)


def main():
    """
    Main command-line argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Uni-Cron task scheduler.")
    args = parser.parse_args()

    handle_tasks()


if __name__ == '__main__':
    main()
