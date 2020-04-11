#!/bin/sh
# Run Unicron as a cron command.
#
# On success, be silent.
# On error, send all output to the user's local mailbox.
#
# This script can be run from anywhere.

SCRIPT_DIR=$(dirname $(realpath $0))
SCRIPT_FILEPATH="$SCRIPT_DIR/../unicron/unicron.py"

OUTPUT="$($SCRIPT_FILEPATH 2>&1)"

if [[ $? -ne 0 ]]; then
    echo "$RESULT" | mail -s 'Unicron task failed!' $USER
fi
