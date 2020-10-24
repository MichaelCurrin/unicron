#!/bin/bash
# Run main app against testing directory using fixture data and show output.
#
# This is a test that should be run and inspected by hand.
# We force it  pass over errors quietly and exit with success status,
# as Unicron will give an exit status if a job fails and that blocks make.

echo "Reset"
echo "==="
./reset.sh
echo
echo

echo "Main - first run"
echo "==="
TEST=true ./unicron.py -v
echo
echo

echo "Main - second run"
echo "==="
TEST=true ./unicron.py -v

true
