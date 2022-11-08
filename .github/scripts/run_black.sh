#!/bin/bash

if python3 -m black app.py model.py controller.py views/ | grep -q 'reformatted'; then
    echo 'black does not seem to have been run. Please run it before pushing'
    exit 1
fi
