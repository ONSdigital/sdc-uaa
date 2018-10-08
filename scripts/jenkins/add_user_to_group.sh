#!/bin/bash

pip install --upgrade pip==18.0
pipenv run pip install pip==18.0
pipenv install requests

pipenv run python ./scripts/add_user_to_group.py -ci admin -cs $ADMIN_SECRET -url $UAA_URL -g surveys.$GROUP_ID -u $USERNAME -v

