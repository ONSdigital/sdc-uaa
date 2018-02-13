#!/bin/bash

# Create Users
pipenv run python add_users.py -ci login -cs loginsecret -url uaa-$SPACE.apps.devtest.onsclofo.uk -u $USERNAME -p $PASSWORD -e jimmy.mcgill@ons.gov.uk -f jimmy -l Bailey -v

# Query User
pipenv run python query_users.py -ci admin -cs adminsecret -url uaa-$SPACE.apps.devtest.onsclofo.uk -u $USERNAME -p $PASSWORD -v

# Add user to group
