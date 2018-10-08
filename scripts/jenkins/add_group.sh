#!/bin/bash

pip install --upgrade pip==18.0
pipenv run pip install pip==18.0
pipenv install requests

pipenv run python ./scripts/create_group.py -ci login -cs $LOGIN_SECRET -url $UAA_URL -g surveys.$GROUP_ID -d $GROUP_NAME -v

