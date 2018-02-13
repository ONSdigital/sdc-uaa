#!/usr/bin/env python3

import argparse
import pprint

import requests


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
        print(f"Access code {access_token}")
    return access_token


def query_client(access_token, url, verbose):

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': f'Bearer {access_token}'}

    response = requests.get(f'http://{url}/oauth/clients', headers=headers)
    if verbose:
        print(response.status_code)
        pprint.pprint(response.json())


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Add user to UAA")
    parser.add_argument("-a", "--admin_id", required=True, dest="admin_id", help="The admin id for the organization")
    parser.add_argument("-s", "--admin_secret", required=True, dest="admin_secret", help="The admin password for the organization")
    parser.add_argument("-url", "--url", required=True, dest="url",
                        help="The UAA url to target")
    parser.add_argument("-v", "--verbose", default=False, required=False, dest="verbose",
                        help="To enable verbose output", action="store_true")

    args = parser.parse_args()

    token = login_admin(args.admin_id, args.admin_secret, args.url, verbose=args.verbose)
    query_client(access_token=token, url=args.url, verbose=args.verbose)

