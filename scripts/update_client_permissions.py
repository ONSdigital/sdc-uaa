import requests
import logging
import argparse

logger = logging.getLogger(__name__)

def login_admin(admin_id, admin_secret, url):
    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Accept': 'application/json'}
    payload = {'grant_type': 'client_credentials',
               'response_type': 'token',
               'token_format': 'opaque'}
    response = requests.post('http://{}/oauth/token'.format(url), headers=headers,
                             params=payload,
                             auth=(admin_id, admin_secret))
    logger.info('Admin login returned {}'.format(response.status_code))
    if response.status_code != 200:
        exit(1)
    resp_json = response.json()
    access_token = resp_json.get('access_token')
    
    return access_token


def update_info(token, url, authorities, authorized_grant_types, client_id, scope):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': 'Bearer {}'.format(token)}

    payload = {'client_id': client_id,
               'authorized_grant_types': authorized_grant_types.split(", "),
               'authorities': authorities.split(", "),
               'scope': authorities.split(", "),
               'resource_ids': 'oauth'}
    
    response = requests.post('http://{}/oauth/clients/response_operations'.format(url))
    logger.info('Update scopes/authorities returned {}'.format(response.status_code))
    if response.status_code != 200:
        exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update permissions of an oauth client")
    parser.add_argument("-a", "--admin_id", required=True, dest="admin_id", help="The admin id for the organization")
    parser.add_argument("-as", "--admin_secret", required=True, dest="admin_secret", help="The admin password for the organization")
    parser.add_argument("-url", "--url", required=True, dest="url",
                        help="The UAA url to target")
    parser.add_argument("-c", "--client_id", required=True, dest="client_id", help="The client ID to update")
    parser.add_argument("-au", "--authorities", required=True, dest="authorities", help="The authorities to grant")
    parser.add_argument("-agt", "--authorized_grant_types", required=True, dest="authorized_grant_types", 
                        help="The authorized grant types to grant")
    parser.add_argument("-sc", "--scope", required=True, dest="scope", help="The scope to grant")

    args = parser.parse_args()

    token = login_admin(args.admin_id, args.admin_secret, args.url)
    update_info(token=token, url=args.url, authorities=args.authorities, authorized_grant_types=args.authorized_grant_types,
                client_id=args.client_id, scope=args.scope)
