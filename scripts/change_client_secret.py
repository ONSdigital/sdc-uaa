#!/usr/bin/env python3

import argparse

import json
import pprint

import requests


def login_admin(admin_id, admin_secret, url, verbose):
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    payload = {'grant_type': 'client_credentials',
               'response_type': 'token',
               'token_format': 'opaque'}
    response = requests.post('http://{}/oauth/token'.format(url), headers=headers,
                             params=payload,
                             auth=(admin_id, admin_secret))
    resp_json = response.json()
    if verbose:
        pprint.pprint(resp_json)
    access_token = resp_json.get('access_token')
    if verbose:
        print("Access code: {}".format(access_token))
    return access_token


def change_secret(access_token, client_id, client_secret, url, verbose):
    client = {
        "clientId": client_id,
        "secret": client_secret,
    }

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer {}'.format(access_token)}

    response = requests.put('http://{0}/oauth/clients/{1}/secret'.format(url, client_id), data=json.dumps(client),
                             headers=headers)
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
    parser.add_argument("-c", "--client_id", required=True, dest="client_id", help="The client id")
    parser.add_argument("-cs", "--client_secret", required=True, dest="client_secret", help="The client password")
    parser.add_argument("-v", "--verbose", default=False, required=False, dest="verbose",
                        help="To enable verbose output", action="store_true")

    args = parser.parse_args()

    token = login_admin(args.admin_id, args.admin_secret, args.url, verbose=args.verbose)
    change_secret(access_token=token, client_id=args.client_id, client_secret=args.client_secret, url=args.url,
                  verbose=args.verbose)
