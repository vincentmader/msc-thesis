#!/bin/sh

# If a virtual environment exists already, remove it.
    [ -d ./venv ] && rm -r ./venv
# Create new virtual environment for python.
    python3 -m venv ./venv
# Enter virtual environment.
    source ./venv/bin/activate;
# Install python-pip3 dependencies.
    pip3 install -r requirements.txt

# Create `./figures` directory, if it does not yet exist.
    [ -d ./figures ] || mkdir -p ./figures
# Create `./data` directory, if it does not yet exist.
    [ -d ./data    ] || mkdir -p ./data
