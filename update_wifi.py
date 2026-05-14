import argparse
import configparser
#import epd4in2
import epd2in7_V2
import os
import pathlib
import qrcode
import random
import subprocess
from arduino_string import sketch_template
from PIL import Image
from router_clients import UnifiClient


def escape_password_for_safety(password):
    password = password.replace('"', '\\"')

    return password


def generate_password(length):
    password = ""

    while len(password) < length:
        # 33-126 is the ascii range of characters that don't give most text fields many problems
        char_num = random.randrange(33, 126)
        password += chr(char_num)

    safe_password = escape_password_for_safety(password)

    print("[+] New password generated")
    return safe_password


def generate_qr_code(wifi_password, screen_width, screen_height):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )

    qr_code_string = f"WIFI:T:WPA;S:{wifi_ssid};P:{wifi_password};;"
    qr.add_data(qr_code_string)
    qr.make()
    img = qr.make_image()
    img = img.resize((screen_width, screen_height))

    print("[+] New QR code generated")
    return img


def updated_trinkey_code(password):
    safe_password = escape_password_for_safety(password)

    return f"""
import time
import board
import digitalio
import neopixel
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
btn = digitalio.DigitalInOut(board.BUTTON)
btn.switch_to_input(pull=digitalio.Pull.UP)

while True:
    # Signal ready — blue means waiting for button press
    pixel.fill((0, 0, 255))

    while btn.value:  # Loop until BOOT is pressed (pulled low)
        time.sleep(0.05)

    # Button pressed - green means button press received
    pixel.fill((0, 0, 255))
    time.sleep(0.5)

    kbd = Keyboard(usb_hid.devices)
    layout = KeyboardLayoutUS(kbd)
    layout.write("{safe_password}")
    time.sleep(0.2)
    kbd.send(Keycode.ENTER)

    # Done — go dark
    pixel.fill((0, 0, 0))
"""


def update_network(wifi_password):
    administration_host = config["NETWORK_ADMINISTRATION"]["host"]
    administration_username = config["NETWORK_ADMINISTRATION"]["username"]
    administration_password = config["NETWORK_ADMINISTRATION"]["password"]
    wifi_id = config["WIFI"]["id"]

    unifi_client = UnifiClient(administration_host, administration_username, administration_password)
    unifi_client.change_wifi_password(wifi_id, wifi_password)
    print(f"[+] Network '{wifi_ssid}' password updated")


def update_screen(screen_instance, img):
    screen_instance.init()
    screen_instance.Clear()
    screen_instance.display(screen_instance.getbuffer(img))

    print("[+] Screen display updated")


def write_code_to_trinkey(wifi_password, mount_path="/media/CIRCUITPY"):
    code = updated_trinkey_code(wifi_password)
    with open(os.path.join(mount_path, "code.py"), "w") as f:
        f.write(code)
    print("[+] Trinkey password typer updated")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--manual', action='store_true')
    parser.add_argument('--v1', action='store_true')
    args = parser.parse_args()
    config = configparser.ConfigParser()
    current_dir = pathlib.Path(__file__).resolve().parent
    config.read(f"{current_dir}/config.ini")
    desired_password_length = int(config["PASSWORD"]["length"])
    wifi_ssid = config["WIFI"]["ssid"]

    #epd = epd4in2.EPD()
    epd = epd2in7_V2.EPD()

    if args.manual:
        new_password = config["PASSWORD"]["value"]
    else:
        new_password = generate_password(desired_password_length)

    qr_code = generate_qr_code(new_password, epd.width, epd.height)
    update_network(new_password)
    update_screen(epd, qr_code)
    if not args.v1:
        write_code_to_trinkey(new_password)
