#!/bin/bash

pipenv install requests

# Create Users
pipenv run python ./scripts/change_client_secret.py -a $ADMIN_ID -as $ADMIN_SECRET -url $UAA_URL -c $CLIENT_ID -cs $CLIENT_SECRET  -v