import argparse
import json
import pprint
import requests


def login_admin(admin_id, admin_secret, url):
    print(admin_id)
    print(admin_secret)
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    payload = {'grant_type': 'client_credentials',
               'response_type': 'token',
               'token_format': 'opaque'}
    response = requests.post(f'http://{url}/oauth/token', headers=headers,
                             params=payload,
                             auth=(admin_id, admin_secret))
    resp_json = response.json()
    pprint.pprint(resp_json)
    access_token = resp_json.get('access_token')
    print(f"Access code{access_token}")
    return access_token


def create_client(access_token, client, client_secret, scope, url):

    client = {
        "client_id": f"{client}",
        "client_secret": f"{client_secret}",
        "authorized_grant_types": ["client_credentials", "password"],
        "scope": f"{scope}",
        "redirect_uri": ["http://ons.gov.uk", "http://ons.gov.uk/**/passback/*"],
    }

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': f'Bearer {access_token}'}

    response = requests.post(f'http://{url}/oauth/clients', data=json.dumps(client),
                             headers=headers)
    print(response.status_code)
    pprint.pprint(response.json())

parser = argparse.ArgumentParser(description="Add user to UAA")
parser.add_argument("-a", "--admin_id", required=True, dest="admin_id", help="The admin id for the organization")
parser.add_argument("-s", "--admin_secret", required=True, dest="admin_secret", help="The admin password for the organization")
parser.add_argument("-url", "--url", required=True, dest="url",
                    help="The UAA url to target")
parser.add_argument("-c", "--client", required=True, dest="client", help="The client id")
parser.add_argument("-p", "--client_password", required=True, dest="password", help="The client password")
parser.add_argument("-sc", "--scope", required=True, dest="scope", help="The client scopes")

args = parser.parse_args()

token = login_admin(args.admin_id, args.admin_secret, args.url)
create_client(access_token=token, client=args.client, client_secret=args.password, url=args.url, scope=args.scope)

