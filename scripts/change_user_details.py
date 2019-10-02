import pprint
import requests
import argparse


def login_admin(admin_id, admin_secret, url, verbose):
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    payload = {'grant_type': 'client_credentials',
               'response_type': 'token',
               'token_format': 'opaque'}
    response = requests.post(f'http://{url}/oauth/token', headers=headers,
                             params=payload,
                             auth=(admin_id, admin_secret))
    resp_json = response.json()
    if verbose:
        pprint.pprint(resp_json)

    access_token = resp_json.get('access_token')

    if verbose:
        print("Access code: {}".format(access_token))

    return access_token


def get_user_by_username(token, username, verbose):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer {}'.format(token)}

    url = f"{url}/Users?filter=userName+eq+%22{username}%22"
    response = requests.get(url, headers=headers)
    if response.status_code != 200 or response.json()['totalResults'] == 0:
        print(f"Couldn't find a user with username {username}")
        exit(1)

    if verbose:
        pprint.pprint(response.json())

    return response.json()['resources'][0]['id']


def update_user_details(token, username, user_code, first_name, last_name, email, verbose):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer {}'.format(token)}
    payload = {'id': user_code,
               'userName': username,
               'name': {'familyName': last_name,
                        'givenName': first_name},
               'emails': [{'value': email,
                           'primary': True}]}
    
    url = f"{url}/Users/{user_code}"
    response = requests.put(url, headers=headers, payload=payload)
    if response.status_code != 200:
        print(f"Error updating user {username} in UAA, status code {response.status_code}")
        exit(1)

    if verbose:
        print(response.status_code)
        pprint.pprint(response.json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Change client secret")
    parser.add_argument("-a", "--admin_id", required=True, dest="admin_id", help="The admin id for the organization")
    parser.add_argument("-as", "--admin_secret", required=True, dest="admin_secret",
                        help="The admin password for the organization")
    parser.add_argument("-url", "--url", required=True, dest="url",
                        help="The UAA url to target")
    parser.add_argument("-u", "--userid", required=True, dest="userid", help="The id of the user requiring a password change")
    parser.add_argument("-f", "--first_name", required=True, dest="first_name", help="The user's first name")
    parser.add_argument("-l", "--last_name", required=True, dest="last_name", help="The user's last name")
    parser.add_argument("-e", "--email", required=True, dest="email", help="The user's email")
    parser.add_argument("-v", "--verbose", default=False, required=False, dest="verbose",
                        help="To enable verbose output", action="store_true")

    args = parser.parse_args()

    # Get an admin access token
    token = login_admin(args.admin_id, args.admin_secret, args.url, verbose=args.verbose)

    # Get the user ID as stored in UAA
    user_code = get_user_by_username(token=token, username=args.userid, verbose=args.verbose)

    update_user_details(token=token, username=args.userid, user_code=user_code, first_name=args.first_name,
                        last_name=args.last_name, email=args.email, verbose=args.verbose)
