"""
Run module.
"""
import datetime
import subprocess
import textwrap
from pathlib import Path
from typing import Optional, Tuple

from . import constants, history, logger, paths


def run_in_shell(cmd: str) -> Tuple[bool, str]:
    """
    Run given command in the shell and return result of the command.

    Usually a malformed command or error in the executed code will result in
    the CalledProcessError and then that message is shown. During development
    of this project, the OSError was experienced so this is covered below too.

    :return success: True if it ran without error, False otherwise.
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


def proccess_cmd_result(
    task_name: str, task_log_path: Path, last_run_path: Path, status: bool, output: str
) -> None:
    """
    Process the result of running a command.

    Log activity for the task and update the last run date if the task was run
    successfully.
    """
    app_logger = logger.setup_logger("unicron", constants.APP_LOG_PATH)
    task_logger = logger.setup_logger(task_name, task_log_path, is_task=True)

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
    last_run_path = paths.mk_last_run_path(task_name)

    task_log_path = paths.mk_output_path(task_name)
    task_logger = logger.setup_logger(task_name, task_log_path, is_task=True)

    task_logger.info("Executing...")
    cmd = constants.TASKS_DIR / task_name
    status, output = run_in_shell(str(cmd))

    proccess_cmd_result(task_name, task_log_path, last_run_path, status, output)

    return status


# Python 3.9 pylint bug https://github.com/PyCQA/pylint/issues/3882
def handle_task(
    task_name: str,
) -> Optional[bool]:  # pylint: disable=unsubscriptable-object
    """
    Run a task, if it still needs to run today.

    :return status: True on task success, False on failure and None on skipped.
    """
    should_run = history.check_need_to_run(task_name)

    if not should_run:
        return None

    return execute(task_name)
