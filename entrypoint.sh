#!/bin/sh

git config --global --add safe.directory '*'
git log | tail -10
/sigridci/sigridci.py "$@"
