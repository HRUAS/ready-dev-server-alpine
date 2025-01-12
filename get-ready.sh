#!/bin/bash

apk add python3
apk add py3-pip

pip3 install boto3
pip3 install awscli --upgrade --user

# Add ~/.local/bin to PATH and persist it
if ! grep -q "export PATH=\$PATH:~/.local/bin" ~/.profile; then
    echo 'export PATH=$PATH:~/.local/bin' >> ~/.profile
fi

# Source the profile to make the change take effect immediately
source ~/.profile
