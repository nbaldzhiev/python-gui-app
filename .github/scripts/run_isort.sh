#!/bin/bash

if python3 -m isort app.py model.py controller.py views/ | grep -o 'Fixing'; then
    echo 'isort does not seem to have been run. Please run it before pushing'
    return 1
fi
