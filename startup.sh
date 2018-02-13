#!/usr/bin/env bash


docker build -t sdc-uaa:0.0.1 .
docker run -d -p 8080:8080 --name sdc-uaa sdc-uaa:0.0.1

sleep 60
cd scripts
./test_setup_local.sh
cd ..

