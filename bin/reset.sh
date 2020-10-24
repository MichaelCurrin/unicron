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

echo 'Create last-run file fixtures.'
cd last_run/
echo $(date +%Y-%m-%d) >today.sh.txt
echo "2020-01-01" >old.sh.txt
rm never_run_before.sh.txt >/dev/null 2>&1 || true
rm fail.sh.txt >/dev/null 2>&1 || true
cd ..

echo 'Remove logs.'
rm app.log >/dev/null 2>&1 || true
rm output/*.log >/dev/null 2>&1 || true
