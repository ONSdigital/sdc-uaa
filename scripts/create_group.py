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


def create_group(access_token, group_name, description, url, verbose):
    group = {
        "displayName": group_name,
        "description": description,
    }

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer {}'.format(access_token)}

    response = requests.post('http://{}/Groups'.format(url), data=json.dumps(group),
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
    parser.add_argument("-g", "--group", required=True, dest="group", help="The group name")
    parser.add_argument("-d", "--description", required=True, dest="description", help="The group description")
    parser.add_argument("-v", "--verbose", default=False, required=False, dest="verbose",
                        help="To enable verbose output", action="store_true")

    args = parser.parse_args()

    token = login_client(client_id=args.client_id, client_secret=args.client_secret, url=args.url, verbose=args.verbose)
    create_group(access_token=token, group_name=args.group, description=args.description, url=args.url,
                 verbose=args.verbose)
