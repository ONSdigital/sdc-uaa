#!/bin/bash

pip install --upgrade pip==18.0
pipenv run pip install pip==18.0
pipenv install requests

# Create a client for RAS backstage
pipenv run python ./scripts/create_client.py -a admin -s $ADMIN_SECRET -url $UAA_URL -c $CLIENT -p $PASSWORD -sc scim.userids,scim.me,scim.read -ca scim.userids,scim.me,scim.read -v
