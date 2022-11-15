import argparse
import configparser
import epd4in2
import os
import qrcode
import random
import subprocess
from arduino_string import sketch_template
from PIL import Image
from router_clients import UnifiClient


def generate_password(length):
    password = ""

    while len(password) < length:
        # 33-126 is the ascii range of characters that don't give most text fields many problems
        char_num = random.randrange(33, 126)
        # 34 is ", 37 is %, 44 is ,, 59 is ; - these sometimes give password fields trouble
        if char_num in [34, 37, 44, 59]:
            continue
        password += chr(char_num)

    print("[+] New password generated")
    return password


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


def update_digispark(wifi_password):
    digispark_sketch = sketch_template.substitute(password=wifi_password)
    try:
        os.mkdir(f"{current_dir}/digispark_sketch")
    except OSError:
        pass

    with open(f"{current_dir}/digispark_sketch/digispark_sketch.ino", "w") as f:
        f.write(digispark_sketch)

    try:
        subprocess.run([
            "arduino-cli",
            "compile",
            "-b",
            "digistump:avr:digispark-tiny",
            "-e",
            "--build-path",
            f"{current_dir}/digispark_sketch/build",
            f"{current_dir}/digispark_sketch/"
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("[-] There was a problem compiling the Arduino sketch")
        exit(1)

    subprocess.Popen([
        "uhubctl",
        "-l",
        "1-1",
        "-a",
        "cycle",
        "-d",
        "5",
    ], stdout=subprocess.DEVNULL)

    subprocess.run(["micronucleus", f"{current_dir}/digispark_sketch/build/digispark_sketch.ino.hex"],
                   stdout=subprocess.DEVNULL)

    print("[+] Digispark password typer updated")


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--manual', action='store_true')
    args = parser.parse_args()
    config = configparser.ConfigParser()
    current_dir = os.path.dirname(os.path.realpath(__file__))
    config.read(f"{current_dir}/config.ini")
    desired_password_length = int(config["PASSWORD"]["length"])
    wifi_ssid = config["WIFI"]["ssid"]

    epd = epd4in2.EPD()

    if args.manual:
        new_password = config["PASSWORD"]["value"]
    else:
        new_password = generate_password(desired_password_length)

    qr_code = generate_qr_code(new_password, epd.width, epd.height)
    update_network(new_password)
    update_screen(epd, qr_code)
    update_digispark(new_password)
