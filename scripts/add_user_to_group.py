import argparse
import json
import pprint
import requests


def login_client(client_id, client_secret, url):
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    payload = {'grant_type': 'client_credentials',
               'response_type': 'token',
               'token_format': 'opaque'}
    response = requests.post(f'http://{url}/oauth/token', headers=headers,
                             params=payload,
                             auth=(client_id, client_secret))
    resp_json = response.json()
    pprint.pprint(resp_json)
    access_token = resp_json.get('access_token')
    print(f"Access code {access_token}")
    return access_token


def query_group(access_token, group, url):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': f'Bearer {access_token}'}

    response = requests.get(f'http://{url}/Groups?filter=displayName+eq+%22{group}%22', headers=headers)
    print(response.status_code)

    json_data = response.json()
    pprint.pprint(response.json())
    group_id = json_data['resources'][0]['id']
    return group_id


def query_user(access_token, username, url):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': f'Bearer {access_token}'}

    response = requests.get(f'http://{url}/Users?filter=userName+eq+%22{username}%22', headers=headers)
    print(response.status_code)

    json_data = response.json()
    print(response.json())
    user_id = json_data['resources'][0]['id']
    return user_id


def add_user_to_group(access_token, user_id, group_id, url):
    user = {"origin": "uaa",
            "type": "USER",
            "value": f"{user_id}"}

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': f'Bearer {access_token}'}

    response = requests.post(f'http://{url}/Groups/{group_id}/members', data=json.dumps(user),
                             headers=headers)
    print(response.status_code)
    pprint.pprint(response.json())


parser = argparse.ArgumentParser(description="Add user to UAA")
parser.add_argument("-ci", "--client_id", required=True, dest="client_id", help="The client id for the organization")
parser.add_argument("-cs", "--client_secret", required=True, dest="client_secret",
                    help="The client password for the organization")
parser.add_argument("-url", "--u-url", required=True, dest="url",
                    help="The UAA url to target")
parser.add_argument("-g", "--group", required=True, dest="group", help="The group name")
parser.add_argument("-u", "--username", required=True, dest="username", help="The username to add to the group")


args = parser.parse_args()

token = login_client(client_id=args.client_id, client_secret=args.client_secret, url=args.url)
group_id = query_group(access_token=token, group=args.group, url=args.url)
user_id = query_user(access_token=token, username=args.username, url=args.url)
add_user_to_group(access_token=token, user_id=user_id, group_id=group_id, url=args.url)