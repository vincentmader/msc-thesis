#!/bin/sh

# Install python-pip3 dependencies.
    pip3 install -r requirements.txt

# Create `./figures` directory, if it does not yet exist.
    [ -d figures ] || mkdir -p ./figures
