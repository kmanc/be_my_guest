#!/usr/bin/python3
import configparser
import os
import requests
import sys

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(f'{dir_path}/config.ini')

administration_host = config["NETWORK_ADMINISTRATION"]["host"]
login_username = config["NETWORK_ADMINISTRATION"]["user"]
login_password = config["NETWORK_ADMINISTRATION"]["password"]
wifi_id = config["WIFI"]["id"]
wifi_new_password = config["PASSWORD"]["value"]

url = f"https://{administration_host}:8443/api/login"
payload = {"username": login_username, "password": login_password}

login = requests.post(url, json=payload)

try:
    assert login.status_code == 200
except AssertionError:
    print("Problem logging in")
    sys.exit()


cookie_parsing = login.headers["Set-Cookie"].split(" ")
for entry in cookie_parsing:
    if "unifises" in entry:
        unifises = entry.split("=")[1]
    if "csrf_token" in entry:
        csrf_token = entry.split("=")[1][:-1]

try:
    assert "unifises" in dict(globals())
    assert "csrf_token" in dict(globals())
except AssertionError:
    print("Problem parsing login response for tokens")
    sys.exit()

url = f"https://{administration_host}:8443/api/s/default/rest/wlanconf/{wifi_id}"
payload = {"x_passphrase": wifi_new_password}
headers = {"Cookie": f"unifises={unifises} csrf_token={csrf_token}"}

change = requests.put(url, json=payload, headers=headers)

try:
    assert change.status_code == 200
    print("Password sucessfully updated")
except AssertionError:
    print("Password update failed")

