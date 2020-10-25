#!/bin/bash -e
# Undo changes made by main file, for easy repeat testing.
#
# This only affects the test var directory so can be run safely.
#
# No action is needed for the fail.sh file since it can never succeed.
# But it is included anyway in case the file is mistakingly created by the main
# script.

echo 'Entering _test_var directory.'
cd unicron/_test_var

echo 'Remove logs.'
rm app.log >/dev/null 2>&1 || true
rm output/*.log >/dev/null 2>&1 || true

echo 'Create last-run file fixtures.'
cd last_run/
# Note that the today.sh task will never actually run when it unicron checks it,
# so there today.sh.log will never get created and this is okay.
echo $(date +%Y-%m-%d) >today.sh.txt
echo "2020-01-01" >old.sh.txt
rm never_run_before.sh.txt >/dev/null 2>&1 || true
rm fail.sh.txt >/dev/null 2>&1 || true
