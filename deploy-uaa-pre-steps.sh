#!/bin/bash

# Set up variables and substitute into the uaa-cf-application.yml file for pushing to Cloud Foundry via Jenkins
# DB details are retrieved from the CF service.  All other variables are stored in the individual Jenkins jobs

cp src/main/resources/uaa-cf-application.yml .

cf login --skip-ssl-validation -u $JENKINS_CF_USERNAME -p $JENKINS_CF_PASSWORD -a $API_ENDPOINT -o $ORG -s $SPACE
cf create-service rds shared-psql postgres-uaa-$SPACE
cf create-service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key
cf service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key

export DB_HOST=$(cf service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key | sed -n 's/.*"host": "\(.*\)",/\1/p')
export DB_NAME=$(cf service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key | sed -n 's/.*"db_name": "\(.*\)",/\1/p')
export DB_USERNAME=$(cf service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key | sed -n 's/.*"username": "\(.*\)"/\1/p')
export DB_PASSWORD=$(cf service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key | sed -n 's/.*"password": "\(.*\)",/\1/p')
export DB_URI="jdbc:postgresql://"$DB_HOST":5432/"$DB_NAME

sed -i -- "s/SPACE/$SPACE/g" uaa-cf-application.yml
sed -i -- "s|DB_URL|${DB_URI}|g" uaa-cf-application.yml
sed -i -- "s/DB_USERNAME/${DB_USERNAME}/g" uaa-cf-application.yml
sed -i -- "s/DB_PASSWORD/${DB_PASSWORD}/g" uaa-cf-application.yml
sed -i -- "s|PRIVATE_KEY_PASSWORD|${UAA_PRIVATE_KEY_PASSWORD}|g" uaa-cf-application.yml
sed -i -- "s|LOGIN_PASSWORD|$LOGIN_PASSWORD|g" uaa-cf-application.yml
sed -i -- "s|UAA_ID|$UAA_ID|g" uaa-cf-application.yml
sed -i -- "s|UAA_SECRET|$UAA_SECRET|g" uaa-cf-application.yml

echo "$UAA_PRIVATE_KEY" > private_key
echo "$UAA_CERTIFICATE" > certificate

sed -e '/PRIVATE_KEY/ {' -e 'r private_key' -e 'd' -e '}' -i uaa-cf-application.yml
sed -e '/CERTIFICATE/ {' -e 'r certificate' -e 'd' -e '}' -i uaa-cf-application.yml