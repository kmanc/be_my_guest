#!/usr/bin/python3
import configparser
import epd1in54_V2
import os
import qrcode
import random
from PIL import Image, ImageDraw, ImageFont


def display_file_image(qr_file_full_path):
	"""
	Takes in a full path of a qr code file and displays it to the e-ink screen.
	Returns nothing.
	"""
	epd = epd1in54_V2.EPD()
	epd.init()
	epd.Clear(0xFF)
	image = Image.open(qr_file_full_path)
	epd.display(epd.getbuffer(image))


def read_config(config_file_full_path):
	"""
	Takes in a full path of a config file and reads it.
	Returns a dictionary containing key/value pairs from the config.
	"""
	config = configparser.ConfigParser()
	config.read(config_file_full_path)
	config_dict = dict()
	config_dict["wifi_ssid"] = config["WIFI"]["ssid"]
	config_dict["desired_password_length"] = int(config["PASSWORD"]["length"])
	desired_qr_size = config["QR_CODE"]["size"]
	config_dict["qr_size_x"] = int(desired_qr_size.split("x")[0])
	config_dict["qr_size_y"] = int(desired_qr_size.split("x")[1])

	return config_dict


def generate_password(desired_password_length):
	"""
	Takes in an integer password length
	Returns a string of input length suitable for Wifi password use
	"""
	password = ""
	while len(password) < desired_password_length:
		# 33-126 is the ascii range of characters that don't give most text fields many problems
		char_num = random.randrange(33, 126)
		# 37 is a % or a ; which give some password fields trouble
		if char_num == 37 or char_num == 59:
			continue
		password += chr(char_num)

	return password


