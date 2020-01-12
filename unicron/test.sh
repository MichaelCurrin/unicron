#!/bin/bash -e
# Run main app against testing directory using fixture data and show output.

export TEST=1

echo "Reset"
echo "==="
./reset.sh
echo
echo

echo "Main - first run"
echo "==="
./unicron.py -v
echo
echo

echo "Main - second run"
echo "==="
./unicron.py -v
