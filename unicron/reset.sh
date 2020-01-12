#!/bin/bash
# Undo changes made by main file, for easy repeat testing.
#
# No action should be needed for the fail.sh file since it can never succeed.
# But it is included anyway in case the file is mistakingly created by the main
# script.

cd _test_var/last_run/

echo $(date +%Y-%m-%d) >today.sh.txt
echo "2020-01-01" >old.sh.txt
rm never_run_before.sh.txt >/dev/null 2>&1 || true
rm fail.sh.txt >/dev/null 2>&1 || true

cd ../output
rm *.log
