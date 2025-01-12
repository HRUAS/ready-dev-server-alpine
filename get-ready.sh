#!/bin/bash

apk add python3
apk add py3-pip

pip3 install boto3
pip3 install awscli --upgrade --user
pip3 install PrettyTable
# Determine the correct shell configuration file
PROFILE_FILE=~/.profile
if [ ! -f "$PROFILE_FILE" ]; then
    PROFILE_FILE=~/.ashrc
fi

# Add ~/.local/bin to PATH and persist it
if ! grep -q "export PATH=\$PATH:~/.local/bin" "$PROFILE_FILE"; then
    echo 'export PATH=$PATH:~/.local/bin' >> "$PROFILE_FILE"
fi

# Source the configuration file to make the change take effect immediately
echo source "$PROFILE_FILE"
