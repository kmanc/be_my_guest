#!/usr/local/bin/python3
import configparser
import os
import ssl
import urllib.parse
import urllib.request

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(f'{dir_path}/config.ini')
wifi_password = config['WIFI']['password']


def make_qr_code(text):
    """Create a computer readable QR code in a PNG format using Google Chart REST API"""
    # https://developers.google.com/chart/infographics/docs/qr_codes
    root_url = 'https://chart.googleapis.com/chart?'
    query = dict(cht='qr', chs='300x300', chl=text)
    url = root_url + urllib.parse.urlencode(query)
    with urllib.request.urlopen(url, context=ssl.SSLContext()) as u:
        qr_image = u.read()
    # According to www.w3.org/TR/PNG/#5PNG-file-signature, first 8 bytes should match
    # 137 80 78 71 13 10 26 10
    try:
        assert qr_image[:8] == bytes([137, 80, 78, 71, 13, 10, 26, 10])
        return qr_image
    except AssertionError:
        print(f'The QR code failed to generate correctly')
        exit(0)


qr = make_qr_code(wifi_password)
with open(f'{dir_path}/wifi_qr.png', 'wb') as image:
    image.write(qr)
