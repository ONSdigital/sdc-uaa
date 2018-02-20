#!/bin/bash

pipenv install requests

# Create Bricks groups
pipenv run python create_group.py -ci login -cs loginsecret -url uaa-$SPACE.apps.devtest.onsclofo.uk -g surveys.073 -d bricks -v

# Create Block groups
pipenv run python create_group.py -ci login -cs loginsecret -url uaa-$SPACE.apps.devtest.onsclofo.uk -g surveys.074 -d blocks -v
