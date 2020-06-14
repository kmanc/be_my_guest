#!/usr/bin/python3
import epd1in54_V2
from PIL import Image, ImageDraw, ImageFont

epd = epd1in54_V2.EPD()
epd.init()
epd.Clear(0xFF)
image = Image.open('wifi_qr.png')
epd.display(epd.getbuffer(image))
