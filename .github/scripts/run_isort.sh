#!/bin/bash

if python3 -m isort app.py | grep -q 'Fixing'; then
    echo 'isort does not seem to have been run. Please run it before pushing'
    exit 1
fi
