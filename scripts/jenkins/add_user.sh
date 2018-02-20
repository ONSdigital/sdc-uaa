#!/bin/bash

pipenv install

# Create Users
pipenv run python ./scripts/add_users.py -ci login -cs loginsecret -url uaa-$SPACE.apps.devtest.onsclofo.uk -u $USERNAME -p $PASSWORD -e $EMAIL -f $FIRSTNAME -l $LASTNAME -v

# Query User
pipenv run python ./scripts/query_users.py -ci admin -cs adminsecret -url uaa-$SPACE.apps.devtest.onsclofo.uk -u $USERNAME -p $PASSWORD -v

