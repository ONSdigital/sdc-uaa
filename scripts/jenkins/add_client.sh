#!/bin/bash

pipenv install requests

# Create a client for RAS backstage
pipenv run python ./scripts/create_client.py -a admin -s $ADMIN_SECRET -url $UAA_URL -c $CLIENT -p $PASSWORD -sc scim.me,scim.read,scim.write,scim.userids,surveys.073,surveys.074,user_attributes,profile -ca clients.read,clients.write,scim.read,scim.write -v
