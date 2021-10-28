import epd4in2
import os
from PIL import Image

dir_path = os.path.dirname(os.path.realpath(__file__))
epd = epd4in2.EPD()
epd.init()
epd.Clear()
image = Image.open(f'{dir_path}/wifi_qr.png')
epd.display(epd.getbuffer(image))
print("Screen display updated")
