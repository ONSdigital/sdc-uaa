#!/bin/bash

pipenv install requests

pipenv run python ./scripts/add_user_to_group.py -ci admin -cs adminsecret -url uaa-$SPACE.apps.devtest.onsclofo.uk -g $GROUP_ID -u $USERNAME -v

