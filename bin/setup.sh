#!/bin/sh

#   Setup virtual environment for python.
#   ───────────────────────────────────────────────────────────────────────────

#   Create virtual environment for python, if it does not exist already.
    [ -d ../venv ] || python3 -m venv ../venv

#   Enter virtual environment.
    source ../venv/bin/activate;

#   Install python-pip3 dependencies.
    pip3 install -r ../requirements.txt


#   Create needed directories.
#   ───────────────────────────────────────────────────────────────────────────

#   Create `../out` directory, if it does not yet exist.
    [ -d ../out ] || mkdir -p ../out

