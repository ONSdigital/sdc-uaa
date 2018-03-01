#!/bin/bash

pipenv install requests

# Create Users
pipenv run python ./scripts/change_user_password.py -a admin -as $ADMIN_SECRET -url $UAA_URL -u $USERID -p $PASSWORD  -v