#!/bin/bash

pip install --upgrade pip==18.0
pipenv run pip install pip==18.0
pipenv install requests

# Create Users
pipenv run python ./scripts/change_user_details.py -a admin -as $ADMIN_SECRET -url $UAA_URL -u $USERID -f $FIRST_NAME -l $LAST_NAME -e $EMAIL -v