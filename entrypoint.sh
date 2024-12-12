#!/bin/sh

git config --global --add safe.directory '*'
/sigridci/sigridci.py $@
