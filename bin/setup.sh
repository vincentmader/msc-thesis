#!/bin/sh

#   Setup virtual environment for python.
#   ───────────────────────────────────────────────────────────────────────────

#   If a virtual environment exists already, remove it.
    [ -d ./venv ] && rm -r ./venv

#   Create new virtual environment for python.
    python3 -m venv ./venv

#   Enter virtual environment.
    source ./venv/bin/activate;

#   Install python-pip3 dependencies.
    pip3 install -r requirements.txt


#   Create needed directories.
#   ───────────────────────────────────────────────────────────────────────────

#   Create `./out/figures` directory, if it does not yet exist.
    [ -d ./out/figures ] || mkdir -p ./out/figures

#   Create `./out/data` directory, if it does not yet exist.
    [ -d ./out/data    ] || mkdir -p ./out/data

