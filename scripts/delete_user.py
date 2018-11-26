#!/usr/bin/env python3

import argparse
import pprint
import sys

import requests


def login_client(client_id, client_secret, url, verbose):
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    payload = {'grant_type': 'client_credentials',
               'response_type': 'token',
               'token_format': 'opaque'}
    response = requests.post('http://{}/oauth/token'.format(url), headers=headers,
                             params=payload,
                             auth=(client_id, client_secret))
    resp_json = response.json()
    if verbose:
        pprint.pprint(resp_json)

    access_token = resp_json.get('access_token')
    if verbose:
        print("Access code {}".format(access_token))

    return access_token


def get_user_id(access_token, username, email, url, verbose):
    if verbose:
        print('Getting user id for username: {0}, email: {1}'.format(username, email))
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer {}'.format(access_token)}

    response = requests.get(url='http://{0}/Users?filter=userName+eq+"{1}"+and+email+eq+"{2}"'.
                            format(url, username, email),
                            headers=headers)

    decoded_json = response.json()
    if verbose:
        print(response.status_code)
        pprint.pprint(decoded_json)

    response.raise_for_status()

    if len(decoded_json['resources']) < 1:
        print('No user found for username: {0}, email: {1}'.format(username, email))
        sys.exit(1)
    elif len(decoded_json['resources']) > 1:
        # Sanity check
        print('ERROR: multiple users found for username: {0}, email: {1}'.format(username, email))
        sys.exit(1)

    if verbose:
        print('Successfully retrieved user id for username: {0}, email: {1}'.format(username, email))

    return decoded_json['resources'][0]['id']


def delete_user(access_token, user_id, url, verbose):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer {}'.format(access_token)}

    response = requests.delete(url='http://{0}/Users/{1}'.format(url, user_id),
                               headers=headers)

    response.raise_for_status()

    if verbose:
        print(response.status_code)
        pprint.pprint(response.json())

    if response.status_code == 200:
        print('Successfully deleted user')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Delete user from UAA")
    parser.add_argument("-ci", "--client_id", required=True, dest="client_id",
                        help="The client id for the organization")
    parser.add_argument("-cs", "--client_secret", required=True, dest="client_secret",
                        help="The client password for the organization")
    parser.add_argument("-url", "--url", required=True, dest="url",
                        help="The UAA url to target")
    parser.add_argument("-u", "--username", required=True, dest="username", help="The username of the user")
    parser.add_argument("-e", "--email", required=True, dest="email", help="The email of the user")
    parser.add_argument("-v", "--verbose", default=False, required=False, dest="verbose",
                        help="To enable verbose output", action="store_true")

    args = parser.parse_args()

    token = login_client(client_id=args.client_id, client_secret=args.client_secret, url=args.url, verbose=args.verbose)
    user_id = get_user_id(access_token=token, username=args.username, email=args.email, url=args.url,
                          verbose=args.verbose)
    delete_user(access_token=token, user_id=user_id, url=args.url, verbose=args.verbose)
