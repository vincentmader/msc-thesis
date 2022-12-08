#!/bin/sh

#   Setup python.
#   ───────────────────────────────────────────────────────────────────────────

#   Make sure required `python3` is installed. Abort if not.
    if ! command -v python3 &> /dev/null; then
        echo "ERROR: python3 could not be found"
        exit
    fi

#   Create virtual environment for python, if it does not exist already.
    [ -d ../venv ] || python3 -m venv ../venv

#   Install python-pip3 dependencies.
    ../venv/bin/pip3 install -r ../requirements.txt


#   Create needed directories.
#   ───────────────────────────────────────────────────────────────────────────

#   Create `../out` directory, if it does not exist already.
    [ -d ../out ] || mkdir ../out

#   Create `../out/runs` directory, if it does not exist already.
    [ -d ../out/runs ] || mkdir ../out/runs


#   Clone repository containing base header-files for LaTeX compilation.
#   ───────────────────────────────────────────────────────────────────────────

#   Define URL & file-path to tex-headers.
    url="https://github.com/vincentmader/tex-headers"
    path="../tex/tex-headers/"

#   Clone repository, if it does not exist already.
    if [ ! -d $path ]; then
        git clone $url $path
#   If it does, pull new changes.
    else
        cd $path && git pull
    fi
