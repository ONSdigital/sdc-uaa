import argparse
import json
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
    access_token = resp_json.get('access_token')
    print(f"Access code{access_token}")
    return access_token


def create_user(access_token, username, password, email, first_name, last_name, url):
    user = {
        "userName": f"{username}",
        "name": {
            "formatted": f"{first_name} {last_name}",
            "familyName": f"{first_name}",
            "givenName": f"{last_name}"
        },
        "emails": [{
            "value": f"{email}",
            "primary": True
        }],
        "phoneNumbers": [{
            "value": "5555555555"
        }],
        "active": True,
        "verified": True,
        "password": f"{password}",
    }

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': f'Bearer {access_token}'}

    response = requests.post(f'http://{url}/Users', data=json.dumps(user),
                             headers=headers)
    print(response.status_code)
    print(response.json())

parser = argparse.ArgumentParser(description="Add user to UAA")
parser.add_argument("-ci", "--client_id", required=True, dest="client_id", help="The client id for the organization")
parser.add_argument("-cs", "--client_secret", required=True, dest="client_secret",
                    help="The client password for the organization")
parser.add_argument("-url", "--u-url", required=True, dest="url",
                    help="The UAA url to target")
parser.add_argument("-u", "--username", required=True, dest="username", help="The username of the user")
parser.add_argument("-p", "--password", required=True, dest="password", help="The password of the user")
parser.add_argument("-e", "--email", required=True, dest="email", help="The email of the user")
parser.add_argument("-f", "--first_name", required=True, dest="first_name", help="The first name of the user")
parser.add_argument("-l", "--last_name", required=True, dest="last_name", help="The last name of the user")

args = parser.parse_args()

token = login_client(client_id=args.client_id, client_secret=args.client_secret, url=args.url)
create_user(access_token=token, username=args.username, password=args.password, email=args.email,
            first_name=args.first_name, last_name=args.last_name, url=args.url)
