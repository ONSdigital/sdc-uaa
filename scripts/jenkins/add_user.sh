#!/bin/bash

pip install --upgrade pip==18.0
pipenv run pip install pip==18.0
pipenv install requests

# Create Users
pipenv run python ./scripts/add_users.py -ci admin -cs $ADMIN_SECRET -url $UAA_URL -u $USERNAME -p $PASSWORD -e $EMAIL -f $FIRSTNAME -l $LASTNAME -v

# Query User
pipenv run python ./scripts/query_users.py -ci admin -cs $ADMIN_SECRET -url $UAA_URL -u $USERNAME -p $PASSWORD -v

