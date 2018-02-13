import argparse
import pprint

import requests


def login_client_and_user(client_id, client_secret, username, password, url, verbose):
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    payload = {'grant_type': 'client_credentials',
               'response_type': 'token',
               'token_format': 'opaque'}
    response = requests.post(
        f'http://{url}/oauth/token?username={username}&password={password}&token_format=opaque&response_type=token',
        headers=headers,
        params=payload,
        auth=(client_id, client_secret))
    resp_json = response.json()
    if verbose:
        pprint.pprint(resp_json)
    access_token = resp_json.get('access_token')
    if verbose:
        print(f"Access code {access_token}")
    return access_token


def query_user(access_token, username, url, verbose):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': f'Bearer {access_token}'}

    response = requests.get(f'http://{url}/Users?filter=userName+eq+%22{username}%22', headers=headers)
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
    parser.add_argument("-v", "--verbose", default=False, required=False, dest="verbose",
                        help="To enable verbose output", action="store_true")

    args = parser.parse_args()

    token = login_client_and_user(client_id=args.client_id, client_secret=args.client_secret, username=args.username,
                                  password=args.password, url=args.url, verbose=args.verbose)

    query_user(access_token=token, username=args.username, url=args.url, verbose=args.verbose)
