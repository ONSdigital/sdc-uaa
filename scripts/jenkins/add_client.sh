#!/bin/bash

pipenv install requests

# Create a client for RAS backstage
pipenv run python ./scripts/create_client.py -a admin -s adminsecret -url $UAA_URL -c $CLIENT -p $PASSWORD -sc scim.me,scim.userids,surveys.073,surveys.074,user_attributes,profile -v
