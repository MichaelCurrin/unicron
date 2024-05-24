"""
Logger module.
"""

import logging
from pathlib import Path


APP_FORMATTER = logging.Formatter(
    "%(asctime)s %(levelname)s:%(filename)s %(task)s - %(message)s"
)
TASK_FORMATTER = logging.Formatter(
    "%(asctime)s %(levelname)s:%(filename)s - %(message)s"
)

VERBOSE = False


def setup_logger(name: str, log_file: Path, is_task: bool = False):
    """
    Configure a logger object and return it.

    It is safe to run this setup multiple in a script as the log filehandler
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
            stream_handler.setLevel(logging.DEBUG if VERBOSE else logging.ERROR)
            logger.addHandler(stream_handler)

    return logger
