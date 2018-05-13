import configparser
import random
import requests
import string

config = configparser.ConfigParser()
config.read('config.ini')
router_ip = config['ROUTER']['ip']
router_username = config['ROUTER']['username']
router_password = config['ROUTER']['password']
wifi_ssid = config['WIFI']['ssid']

new_pass = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=60))
post_dict = {'PrimaryNetworkEnable': 1,
             'ServiceSetIdentifier': wifi_ssid,
             'ClosedNetwork': 0,
             'BssModeRequired': 0,
             'WpaPskAuth': 0,
             'Wpa2PskAuth': 1,
             'WpaEncryption': 2,
             'WpaPreSharedKey': new_pass,
             'ShowWpaKey': 0x01,
             'PlainTextKey': '',
             'EncryptedKey': '',
             'WpaRekeyInterval': 0,
             'GenerateWepKeys': 0,
             'WepKeysGenerated': 0,
             'commitwlanPrimaryNetwork': 1,
             'AutoSecurity': 1}

response = requests.post(f'http://{router_ip}/goform/wlanPrimaryNetwork',
                         data=post_dict,
                         auth=(router_username, router_password))
try:
    assert response.status_code == 200
    print(f'Wifi password was successfully altered')
except AssertionError:
    print(f'Wifi password could not be changed, received a {response.status_code} from the router POST')
