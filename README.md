# SDC-UAA

Build the docker images using:

docker build -t sdc-uaa .

Run the container providing the spring profiles in CATALINA_OPTS

docker run -p 8080:8080 -e CATALINA_OPTS="-Dspring.profiles.active=default,hsqldb" sdc-uaa

# sdc-uaa endpoints

There are a number of helper scripts to set up uaa that act as wrappers to make hitting uaa endpoints easier. For full information on the endpoints visit https://docs.cloudfoundry.org/api/uaa/

Below is a brief description on what hitting each of these endpoints does.

Endpoint: `/oauth/token`
* POST request to this endpoint logs in a client, admin, or user.

### Create group script
This script is used to add groups to the UAA. To do this, you need to supply the cloud foundry space, group ID, group name, and log-in secret.

Endpoint: `/Groups`
* GET request to this endpoint shows the results of a group search query.
* POST request to this endpoint creates a new group

### Add user script
This script is used to add users to the UAA. To do this, you need to supply the username, first name, last name, e-mail, password, admin secret, and the cloud foundry space.

Endpoint: `/Users`
* GET request to this endpoint shows the results of a user search query.
* POST request to this endpoint creates a new user.

### Add users to group script
This script is used to add users to a group. To do this, you need to supply the cloud foundry space, group ID, and username.

Endpoint: `/Groups/<group_id>/members`
* POST request to this endpoint adds a user to a group.
* `group_id` is the ID of the group.

### Change client secret script
This script is used to change a client's secret password. To do this, you need to supply cloud foundry space, the admin secret, the client ID, and the client secret.

Endpoint: `/oauth/clients/<client_id>/secret`
* PUT request to this endpoint changes the client's password to the organisation.
* `client_id` is the ID of the client.

### Change user password script
This script is used to change the user's password for the UAA. To do this, you need to supply the cloud foundry space, admin secret, username, and password.

Endpoint: `/password_change`
* POST request to this endpoint changes a password.

### Create new client script
This script is used to create a new client. To do this, you need to supply the cloud foundry space, client name, password, and admin secret.

Endpoint: `/oauth/clients`
* POST request to this endpoint creates a new client.

### Delete user script
This script is used to delete the user from the UAA. To do this, you need to supply the cloud foundry space, username, e-mail, and admin secret.

Endpoint: `/Users/<user_id>`
* DELETE request to this endpoint deletes a user.
* `user_id` is the ID of the user.

### Query client script
This script is used to get the client information. To do this, you need to supply the username, password, client ID, and client password.

Endpoint: `/oauth/clients`
* GET request to this endpoint shows the results of a client search query.