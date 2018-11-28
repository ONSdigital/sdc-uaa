#!/bin/bash

pip install --upgrade pip==18.0
pipenv run pip install pip==18.0
pipenv install requests

# Delete user
pipenv run python ./scripts/delete_user.py -ci admin -cs $ADMIN_SECRET -url $UAA_URL -u $USERNAME -e $EMAIL -v
