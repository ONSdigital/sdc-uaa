#!/bin/bash

# Example script for adding users to the UAA

# Create a client for RAS backstage
pipenv run python create_client.py -a admin -s adminsecret -url uaa-int.apps.devtest.onsclofo.uk -c ras_backstage -p password -sc scim.me,scim.userids,073,074,user_attributes,profile -v

# Create a client for Secure Message
pipenv run python create_client.py -a admin -s adminsecret -url uaa-int.apps.devtest.onsclofo.uk -c secure_message -p password -sc scim.me,scim.userids,073,074,user_attributes,profile -v

# Create Bricks groups
pipenv run python create_group.py -ci login -cs loginsecret -url uaa-int.apps.devtest.onsclofo.uk -g 073 -d bricks -v

# Create Block groups
pipenv run python create_group.py -ci login -cs loginsecret -url uaa-int.apps.devtest.onsclofo.uk -g 074 -d blocks -v

# Create Users
pipenv run python add_users.py -ci login -cs loginsecret -url uaa-int.apps.devtest.onsclofo.uk -u jimmy -p password -e jimmy.mcgill@ons.gov.uk -f jimmy -l mcgill -v

# Query User
pipenv run python query_users.py -ci admin -cs adminsecret -url uaa-int.apps.devtest.onsclofo.uk -u jimmy -p password -v

# Add user to group
pipenv run python add_user_to_group.py -ci admin -cs adminsecret -url uaa-int.apps.devtest.onsclofo.uk -g 073 -u jimmy -v

# Add user to group
pipenv run python add_user_to_group.py -ci admin -cs adminsecret -url uaa-int.apps.devtest.onsclofo.uk -g 074 -u jimmy -v