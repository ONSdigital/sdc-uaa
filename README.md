# SDC-UAA

Build the docker images using:

docker build -t sdc-uaa .

Run the container providing the spring profiles in CATALINA_OPTS

docker run -p 8080:8080 -e CATALINA_OPTS="-Dspring.profiles.active=default,hsqldb" sdc-uaa

