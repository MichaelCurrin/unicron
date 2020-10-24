#!/bin/bash
# Run app in VERBOSE mode against the isolated TEST VAR directory.
#
# This is a test that should be run and inspected by hand. It has little benefit in CI.
# We forcing pass over errors quietly and exit with success status,
# as Unicron will give an exit status if a job fails and that blocks make.

echo "Main - first run"
echo "==="
TEST=true unicron/unicron.py -v
echo
echo

echo "Main - second run"
echo "==="
TEST=true unicron/unicron.py -v

true
