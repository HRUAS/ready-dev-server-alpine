#!/bin/bash

apk add python3

apk add py3-pip

pip3 install boto3
pip3 install awscli --upgrade --user

export PATH=$PATH:~/.local/bin
