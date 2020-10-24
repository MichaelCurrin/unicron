#!/bin/bash
# Run Unicron as a scheduled cron command.
#
# This script can be run from anywhere.
#
# On success, run silently - nothing printed at all.
# On error, capture all stdout and stderr so it can be sent to user's local mailbox using cron's mechanism or the mail command.
# Either way, you won't see anything printed if run this command.

set -e

SCRIPT_DIR=$(dirname $(dirname $(realpath $0)))

cd "$SCRIPT_DIR"

set +e

CMD_OUTPUT="$(make run-quiet 2>&1)"

if [[ $? -ne 0 ]]; then
  set -e
  echo "$CMD_OUTPUT" | mail -s 'Unicron task failed!' $USER

  exit 1
fi

exit 0
