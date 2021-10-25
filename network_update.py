#!/usr/bin/python3
import configparser
import os
import requests
import sys

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(f'{dir_path}/config.ini')

administration_host = config["NETWORK_ADMINISTRATION"]["host"]
login_username = config["NETWORK_ADMINISTRATION"]["username"]
login_password = config["NETWORK_ADMINISTRATION"]["password"]
wifi_id = config["WIFI"]["id"]
wifi_new_password = config["PASSWORD"]["value"]


def create_client(login_url, login_payload):
    session = requests.Session()
    session.verify = False
    login = session.post(login_url, json=login_payload, verify=False)
    if login.status_code != 200:
        print("Problem logging in")
        sys.exit()

    token_needs_parsing = login.headers.get("Set-Cookie")

    try:
        token = token_needs_parsing.split(";")[0]
    except AttributeError:
        print("Set-Cookie token not found in login response")
        sys.exit()
    except SyntaxError:
        print("Token value found is not a string")
        sys.exit()

    csrf_token = login.headers.get("x-csrf-token")

    if csrf_token is None:
        print("CSRF token not found in login response")
        sys.exit()

    session.headers.update({"Cookie": token, "x-csrf-token": csrf_token})

    return session


auth_endpoint = f"https://{administration_host}:443/api/auth/login"
auth_params = {"username": login_username, "password": login_password}
unifi_client = create_client(auth_endpoint, auth_params)
network_url = f"https://{administration_host}:443/proxy/network/api/s/default/rest/wlanconf/{wifi_id}"
network_payload = {"x_passphrase": wifi_new_password}

change = unifi_client.put(network_url, json=network_payload)

if change.status_code == 200:
    print("Network password successfully updated")
else:
    print("Network password update failed")

