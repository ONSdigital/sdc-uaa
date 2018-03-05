#!/usr/bin/env python3

import argparse
import json
import pprint

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


def create_user(access_token, username, password, email, first_name, last_name, url, verbose):
    user = {
        "userName": "{}".format(username),
        "name": {
            "formatted": "{0} {1}".format(first_name, last_name),
            "givenName": first_name,
            "familyName": last_name
        },
        "emails": [{
            "value": email,
            "primary": True
        }],
        "active": True,
        "verified": True,
        "password": password
    }

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer {}'.format(access_token)}

    response = requests.post('http://{}/Users'.format(url), data=json.dumps(user),
                             headers=headers)
    if verbose:
        print(response.status_code)
        pprint.pprint(response.json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Add user to UAA")
    parser.add_argument("-ci", "--client_id", required=True, dest="client_id",
                        help="The client id for the organization")
    parser.add_argument("-cs", "--client_secret", required=True, dest="client_secret",
                        help="The client password for the organization")
    parser.add_argument("-url", "--u-url", required=True, dest="url",
                        help="The UAA url to target")
    parser.add_argument("-u", "--username", required=True, dest="username", help="The username of the user")
    parser.add_argument("-p", "--password", required=True, dest="password", help="The password of the user")
    parser.add_argument("-e", "--email", required=True, dest="email", help="The email of the user")
    parser.add_argument("-f", "--first_name", required=True, dest="first_name", help="The first name of the user")
    parser.add_argument("-l", "--last_name", required=True, dest="last_name", help="The last name of the user")
    parser.add_argument("-v", "--verbose", default=False, required=False, dest="verbose",
                        help="To enable verbose output", action="store_true")

    args = parser.parse_args()

    token = login_client(client_id=args.client_id, client_secret=args.client_secret, url=args.url, verbose=args.verbose)
    create_user(access_token=token, username=args.username, password=args.password, email=args.email,
                first_name=args.first_name, last_name=args.last_name, url=args.url, verbose=args.verbose)
