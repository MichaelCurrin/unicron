#!/bin/bash -e
# Run main app against testing directory using fixture data and show output.

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
