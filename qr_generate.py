import configparser
import os
import qrcode

config = configparser.ConfigParser()
dir_path = os.path.dirname(os.path.realpath(__file__))
config.read(f'{dir_path}/config.ini')

wifi_ssid = config["WIFI"]["ssid"]
wifi_password = config["PASSWORD"]["value"]
desired_qr_size = config["QR_CODE"]["size"]
qr_size_x = int(desired_qr_size.split("x")[0])
qr_size_y = int(desired_qr_size.split("x")[1])

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
img = img.resize((qr_size_x, qr_size_y))
img.save(f"{dir_path}/wifi_qr.png")

print("New QR code generated and written to file")
