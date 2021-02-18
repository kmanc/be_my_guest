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

url = f"https://{administration_host}:443/api/auth/login"
payload = {"username": login_username, "password": login_password}

login = requests.post(url, json=payload, verify=False)

try:
    assert login.status_code == 200
except AssertionError:
    print("Problem logging in")
    sys.exit()

token = login.headers.get("Set-Cookie").split(";")[0]
csrf_token = login.headers.get("x-csrf-token")

try:
    assert token is not None
    assert csrf_token is not None
except AssertionError:
    print("Problem parsing login response for tokens")
    sys.exit()

url = f"https://{administration_host}:443/proxy/network/api/s/default/rest/wlanconf/{wifi_id}"
payload = {"x_passphrase": wifi_new_password}
headers = {"Cookie": token, "x-csrf-token": csrf_token}
change = requests.put(url, json=payload, headers=headers, verify=False)

try:
    assert change.status_code == 200
    print("Password sucessfully updated")
except AssertionError:
    print("Password update failed")

