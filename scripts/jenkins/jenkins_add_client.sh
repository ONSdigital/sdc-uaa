#!/bin/bash

# Create a client for RAS backstage
pipenv run python create_client.py -a admin -s adminsecret -url uaa-int.apps.devtest.onsclofo.uk -c ras_backstage -p password -sc scim.me,scim.userids,surveys.073,surveys.074,user_attributes,profile -v
