#!/bin/bash -e
# Uni-Cron main script.
#
# Run targeted executables. If this main script is run multiple times in a day, it will still
# only execute each script once, or as many times as it takes to get a success.
#
# How it works:
#   Iterate through files in the configured targets directory. These should all be executables.
#   If there is a record that says the executable has not run today, then run it and on success
#   then add record that it ran today. If the script fails, leave the record as it was.
#
# This script uses levels of debugging to make viewing and filtering the log files easier.
#   DEBUG: Low-priorty message which can normally be ignored. Used during development and
#       debugging the main script. By default, these messages are always logged but not printed.
#   INFO: Standard message.
#   ERROR: Critical message.

# Environment variables:
#   TEST: Set this to a non-empty value to run in test mode. This runs again an alternate directory
#       instead of 'var'.
#   VERBOSE: Set this to a non-empty value such as 1 to make the application print the DEBUG
#       messages which are hidden.

# TODO: Check executable status.

# TODO: Get path to this file
# TODO: later - create lock file for it

# read tasks from targets list. In future this can be symlinks.
# don't need to lock individual tasks as they go in sequence.

# TODO: start with main script's dir so this can run from anywhere.
# TODO: Change to test dir for tests.
if [[ -n "$TEST" ]]; then
    echo "Running in test mode."
    VAR_DIR='_test_var'
else
    VAR_DIR='var'
fi

LAST_RUN_NAME='last_run'
LAST_RUN_DIR="$VAR_DIR/$LAST_RUN_NAME"
TARGET_DIR="$VAR_DIR/targets"
RUN_EXT='.txt'
OUTPUT_DIR="$VAR_DIR/output"
APP_LOG_PATH="$VAR_DIR/app.log"

today() {
    echo $(date +%Y%m%d)
}

now() {
    echo $(date '+%Y-%m-%d %H:%M:%S')
}

log() {
    if [ "$#" -ne 3 ]; then
        echo "Error: Incorrect args count for log! Expected 3 but got: $#."
        echo "Aborting script!"
        exit 1
    fi
    local LEVEL=$1
    local NAME=$2
    local MSG=$3
    LOG_MSG="$(now) $LEVEL:$(basename $0) $NAME - $MSG"

    echo "$LOG_MSG" >>"$APP_LOG_PATH"
    if [[ "$LEVEL" != 'DEBUG' ]] || [[ -n "$DEBUG" ]]; then
        echo "$LOG_MSG"
    fi
}

execute_file() {
    # On a succesful run, set today's date in the last run event file for the executable, so
    # that on subsequent runs today this executable will be ignored.
    # On a failing run, do not update the file so we leave it marked as need to run today still.
    #
    # Regardless of the executed file's output, capture all output and send it
    # to a log file dedicated to that file. This makes it easy to view the executable's history
    # later.
    if [ "$#" -ne 2 ]; then
        echo "Error: Incorrect args count for execute_file! Expected 2 but got: $#."
        exit 1
    fi

    local TARGET_NAME="$1"
    local LAST_RUN_PATH="$2"

    local CMD="$TARGET_DIR/$TARGET_NAME"
    local LOG_PATH="$OUTPUT_DIR/$TARGET_NAME.log"

    log "DEBUG" "$TARGET_NAME" "Running command: '$CMD'."

    echo -e "$(now) - Executing...\n\n" >>$LOG_PATH

    set +e
    # TODO: capture all output and write, do not print to main script's console.
    $CMD >>$LOG_PATH 2>&1
    if [ $? -eq 0 ]; then
        log "INFO" "$TARGET_NAME" "Success."
        echo $(today) >"$LAST_RUN_PATH"
    else
        log "ERROR" "$TARGET_NAME" "Exited with error! Check the log: $LOG_PATH"
        # TODO: Send mail to user with helpful message and output.
    fi
    set -e
}

for TARGET_NAME in $(cd $TARGET_DIR && ls *); do
    LAST_RUN_PATH=$LAST_RUN_DIR/$TARGET_NAME$RUN_EXT

    if [ -f $LAST_RUN_PATH ]; then
        RUN_DATE=$(<$LAST_RUN_PATH)

        if [ "$RUN_DATE" -lt "$(today)" ]; then
            log "DEBUG" "$TARGET_NAME" "Executing, since run file's date is old."
        else
            log "INFO" "$TARGET_NAME" "Skipping, since already ran today."
            continue
        fi
    else
        log "DEBUG" "$TARGET_NAME" "Executing, since run file is missing."
    fi

    execute_file "$TARGET_NAME" "$LAST_RUN_PATH"

    echo "---"
done
