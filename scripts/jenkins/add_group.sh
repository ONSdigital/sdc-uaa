#!/bin/bash

pipenv install requests

pipenv run python ./scripts/create_group.py -ci login -cs loginsecret -url $UAA_URL -g surveys.$GROUP_ID -d $GROUP_NAME -v

