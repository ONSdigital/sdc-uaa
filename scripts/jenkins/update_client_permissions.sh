#!/bin/bash

pip install --upgrade pip==18.0
pipenv run pip install pip==18.0
pipenv install requests

# Create Users
pipenv run python ./scripts/update_client_permissions.py -a admin -as $ADMIN_SECRET -url $UAA_URL -c $CLIENT_ID -au $AUTHORITIES -agt $GRANT_TYPES -sc $SCOPE