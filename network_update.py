#!/usr/bin/python3
import configparser
import os
import requests

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(f'{dir_path}/config.ini')

administration_host = config["NETWORK_ADMINISTRATION"]["host"]
login_username = config["NETWORK_ADMINISTRATION"]["username"]
login_password = config["NETWORK_ADMINISTRATION"]["password"]
wifi_id = config["WIFI"]["id"]
wifi_new_password = config["PASSWORD"]["value"]


class UnifiAuthorizationError(Exception):
    pass


class UnifiInstantiationError(Exception):
    pass


def create_unifi_client(login_url, login_payload, verify_requests=False):
    session = requests.Session()
    session.verify = verify_requests
    login = session.post(login_url, json=login_payload)
    if login.status_code != 200:
        raise UnifiAuthorizationError("Problem logging in to the cloud key")

    try:
        cookie = login.headers.get("Set-Cookie").split(";")[0]
    except AttributeError:
        raise UnifiInstantiationError("Set-Cookie token not found in login response")
    except SyntaxError:
        raise UnifiInstantiationError("Token value found is not a string")

    csrf_token = login.headers.get("x-csrf-token")
    if csrf_token is None:
        raise UnifiInstantiationError("CSRF token not found in login response")

    session.headers.update({"Cookie": cookie, "x-csrf-token": csrf_token})

    return session


auth_endpoint = f"https://{administration_host}:443/api/auth/login"
auth_params = {"username": login_username, "password": login_password}
unifi_client = create_unifi_client(auth_endpoint, auth_params)
network_url = f"https://{administration_host}:443/proxy/network/api/s/default/rest/wlanconf/{wifi_id}"
network_payload = {"x_passphrase": wifi_new_password}

change = unifi_client.put(network_url, json=network_payload)

if change.status_code == 200:
    print("Network password successfully updated")
else:
    print("Network password update failed")

