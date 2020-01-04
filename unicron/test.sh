#!/bin/bash -e

export TEST=1

echo "Reset"
echo "==="
./reset.sh
echo
echo

echo "Main - first run"
echo "==="
./unicron.sh
echo
echo

echo "Main - second run"
echo "==="
./unicron.sh
