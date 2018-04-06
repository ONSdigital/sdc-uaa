#!/bin/bash

# Set up variables and substitute into the uaa-cf-application.yml file for pushing to Cloud Foundry via Jenkins
# DB details are retrieved from the CF service.  All other variables are stored in the individual Jenkins jobs

cp src/main/resources/uaa-cf-application.yml .

#Create DB and resolve connection details if in dev mode.  In prod/preprod, these will come directly from Jenkins
if [ ${#} -eq 1 ] && [ $1 = 'dev' ]
then
    cf login --skip-ssl-validation -u $JENKINS_CF_USERNAME -p $JENKINS_CF_PASSWORD -a $API_ENDPOINT -o $ORG -s $SPACE
    cf create-service rds shared-psql postgres-uaa-$SPACE
    cf create-service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key
    cf service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key

    export DB_HOST=$(cf service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key | sed -n 's/.*"host": "\(.*\)",/\1/p')
    export DB_NAME=$(cf service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key | sed -n 's/.*"db_name": "\(.*\)",/\1/p')
    export DB_USERNAME=$(cf service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key | sed -n 's/.*"username": "\(.*\)"/\1/p')
    export DB_PASSWORD=$(cf service-key postgres-uaa-$SPACE postgres-uaa-$SPACE-key | sed -n 's/.*"password": "\(.*\)",/\1/p')
    export DB_URI="jdbc:postgresql://"$DB_HOST":5432/"$DB_NAME
fi

sed -i -- "s/SPACE/$SPACE/g" uaa-cf-application.yml
sed -i -- "s|DB_URL|${DB_URI}|g" uaa-cf-application.yml
sed -i -- "s/DB_USERNAME/${DB_USERNAME}/g" uaa-cf-application.yml
sed -i -- "s/DB_PASSWORD/${DB_PASSWORD}/g" uaa-cf-application.yml
sed -i -- "s|PRIVATE_KEY_PASSWORD|${UAA_PRIVATE_KEY_PASSWORD}|g" uaa-cf-application.yml
sed -i -- "s|UAA_ID|$UAA_ID|g" uaa-cf-application.yml
sed -i -- "s|UAA_SECRET|$UAA_SECRET|g" uaa-cf-application.yml
sed -i -- "s|UAA-URL|$UAA_URL|g" uaa-cf-application.yml
sed -i -- "s|LOGIN-URL|$LOGIN_URL|g" uaa-cf-application.yml
sed -i -- "s|ZONE-URL|$ZONE_URL|g" uaa-cf-application.yml
sed -i -- "s/ADMIN_SECRET/$ADMIN_SECRET/g" uaa-cf-application.yml
sed -i -- "s/LOGIN_SECRET/$LOGIN_SECRET/g" uaa-cf-application.yml

echo "$UAA_PRIVATE_KEY" > private_key
echo "$UAA_CERTIFICATE" > certificate
echo "$UAA_JWT_SIGNING_KEY" > jwt_signing_key
echo "$UAA_JWT_VERIFICATION_KEY" > jwt_verification_key


sed -e '/PRIVATE_KEY/ {' -e 'r private_key' -e 'd' -e '}' -i uaa-cf-application.yml
sed -e '/CERTIFICATE/ {' -e 'r certificate' -e 'd' -e '}' -i uaa-cf-application.yml
sed -e '/SIGNING_KEY/ {' -e 'r jwt_signing_key' -e 'd' -e '}' -i uaa-cf-application.yml
sed -e '/VERIFICATION_KEY/ {' -e 'r jwt_verification_key' -e 'd' -e '}' -i uaa-cf-application.yml