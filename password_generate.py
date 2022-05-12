import configparser
import os
import random

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(f'{dir_path}/config.ini')

desired_password_length = int(config["PASSWORD"]["length"])


def generate_password(length):
    password = ""

    while len(password) < length:
        # 33-126 is the ascii range of characters that don't give most text fields many problems
        char_num = random.randrange(33, 126)
        # 34 is ", 37 is %, 44 is ,, 59 is ; - these sometimes give password fields trouble
        if char_num in [34, 37, 44, 59]:
            continue
        password += chr(char_num)

    return password


wifi_password = generate_password(desired_password_length)
config['PASSWORD']["value"] = wifi_password
with open(f'{dir_path}/config.ini', 'w') as f:
    config.write(f)

print("New password generated and written to config")
