#!/bin/bash

pip install --upgrade pip==18.0
pipenv run pip install pip==18.0
pipenv install requests

# Create Users
pipenv run python ./scripts/change_client_secret.py -a admin -as $ADMIN_SECRET -url $UAA_URL -c $CLIENT_ID -cs $CLIENT_SECRET  -v