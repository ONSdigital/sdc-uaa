# SDC-UAA

Build the docker images using:

docker build -t sdc-uaa .

Run the container providing the spring profiles in CATALINA_OPTS

docker run -p 8080:8080 -e CATALINA_OPTS="-Dspring.profiles.active=default,hsqldb" sdc-uaa

# sdc-uaa endpoints

This page documents the sdc-uaa endpoints that can be hit.

`/oauth/token`
* POST request to this endpoint logs in a client, admin, or user.

`/Groups`
* GET request to this endpoint shows the results of a group search query.
* POST request to this endpoint creates a new group

`/Users`
* GET request to this endpoint shows the results of a user search query.
* POST request to this endpoint creates a new user.

`/Groups/<group_id>/members`
* POST request to this endpoint adds a user to a group.
* `group_id` is the ID of the group.

`/oauth/clients/<client_id>/secret`
* PUT request to this endpoint changes the client's password to the organisation.
* `client_id` is the ID of the client.

`/password_change`
* POST request to this endpoint changes a password.

`/oauth/clients`
* POST request to this endpoint creates a new client.

`/Users/<user_id>`
* DELETE request to this endpoint deletes a user.
* `user_id` is the ID of the user.

`/oauth/clients`
* GET request to this endpoint shows the results of a client search query.