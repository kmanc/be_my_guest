#!/usr/bin/python3
import epd4in2
from PIL import Image, ImageDraw, ImageFont

epd = epd4in2.EPD()
epd.init()
epd.Clear(0xFF)
image = Image.open('wifi_qr.png')
epd.display(epd.getbuffer(image))
print("Screen display updated")
