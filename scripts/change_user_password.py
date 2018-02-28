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


def retrieve_user_code(access_token, userid, url, verbose):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer {}'.format(access_token)}

    response = requests.post('http://{}/password_resets'.format(url), headers=headers,
                             data=userid)

    resp_json = response.json()
    if verbose:
        pprint.pprint(resp_json)
    
    user_code = resp_json.get('code')

    if verbose:
        print("User code: {}".format(user_code))
    
    return user_code


def change_password(access_token, user_code, new_password, url, verbose):
    password = {
        "code": user_code,
        "new_password": new_password,
    }

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer {}'.format(access_token)}

    response = requests.post('http://{}/password_change'.format(url), data=json.dumps(password),
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
    parser.add_argument("-u", "--userid", required=True, dest="userid", help="The id of the user requiring a password change")
    parser.add_argument("-p", "--new_password", required=True, dest="new_password", help="The new password for the user")
    parser.add_argument("-v", "--verbose", default=False, required=False, dest="verbose",
                        help="To enable verbose output", action="store_true")

    args = parser.parse_args()

    token = login_admin(args.admin_id, args.admin_secret, args.url, verbose=args.verbose)
    user_code = retrieve_user_code(access_token=token, userid=args.userid, url=args.url, verbose=args.verbose)
    change_password(access_token=token, user_code=user_code, new_password=args.new_password, url=args.url,
                  verbose=args.verbose)
