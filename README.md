# UUA Spin up via Docker Image. 

## Setup

The docker file Dockerfile, will install all the required software: 

    Java 8
    apache-tomcat-8.5.27
    cloudfoundry-identity-uaa-2.7.1
    
The application will be deployed in  /tomcat/webapps/ and renamed as ROOT.war. 

## Dependencies 
The application need a
 
    postgress database running 
    uaa.yml that contains the basic configuration. 
 
##Docker 

Postgres needs to be started before using a standard postgres user:

     docker run -d --name uaa-db postgres
 
The UAA application will run on the 8080 port, and needs to be linked to the postgres image uaa-db, therefore:
 
    docker run  -p 8080:8080 --link uaa-db:db -v /tmp/uaa:/uaa:rw ons-uaa

