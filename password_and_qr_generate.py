#!/usr/bin/python3
import configparser
import os
import qrcode
import random
from PIL import Image

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(f'{dir_path}/config.ini')

wifi_ssid = config["WIFI"]["ssid"]
desired_password_length = int(config["PASSWORD"]["length"])
desired_qr_size = config["QR_CODE"]["size"]
qr_size_x = int(desired_qr_size.split("x")[0])
qr_size_y = int(desired_qr_size.split("x")[1])

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=0,
)

wifi_password = ""

while len(wifi_password) < desired_password_length:
    # 33-126 is the ascii range of characters that don't give most text fields many problems
    char_num = random.randrange(33, 126)
    # 37 is a % which gives some password fields trouble
    if char_num == 37:
        continue
    wifi_password += chr(char_num)

config['PASSWORD']["value"] = wifi_password
with open(f'{dir_path}/config.ini', 'w') as f:
    config.write(f)

qr_code_string = f"WIFI:T:WPA;S:{wifi_ssid};P:{wifi_password};;"
qr.add_data(qr_code_string)
qr.make()
img = qr.make_image()
img = img.resize((qr_size_x, qr_size_y))
img.save(f"{dir_path}/wifi_qr.png")
print("New password generated and written to config")
