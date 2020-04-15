#!/bin/bash
# Run Unicron as a cron command.
#
# On success, be silent.
# On error, send all output to the user's local mailbox.
#
# This script can be run from anywhere.

set -e

SCRIPT_DIR=$(dirname $(realpath $0))
SCRIPT_FILEPATH="$SCRIPT_DIR/../unicron/unicron.py"

set +e
OUTPUT="$($SCRIPT_FILEPATH 2>&1)"

if [[ $? -ne 0 ]]; then
    set -e
    echo "$RESULT" | mail -s 'Unicron task failed!' $USER

    exit 1
fi

exit 0
