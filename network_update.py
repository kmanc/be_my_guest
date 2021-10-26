#!/usr/bin/python3
import configparser
import os
from router_clients import UnifiClient

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(f'{dir_path}/config.ini')

administration_host = config["NETWORK_ADMINISTRATION"]["host"]
login_username = config["NETWORK_ADMINISTRATION"]["username"]
login_password = config["NETWORK_ADMINISTRATION"]["password"]
wifi_id = config["WIFI"]["id"]
wifi_new_password = config["PASSWORD"]["value"]

unifi_client = UnifiClient(administration_host, login_username, login_password)
unifi_client.change_wifi_password(wifi_id, wifi_new_password)
print(f"Network '{wifi_id}' password updated")
