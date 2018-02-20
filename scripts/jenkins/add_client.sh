#!/bin/bash

pipenv install

# Create a client for RAS backstage
pipenv run python ./scripts/create_client.py -a admin -s adminsecret -url uaa-$SPACE.apps.devtest.onsclofo.uk -c $CLIENT -p $PASSWORD -sc scim.me,scim.userids,surveys.073,surveys.074,user_attributes,profile -v
