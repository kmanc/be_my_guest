---
title: "Wifi QR"
---

# Wifi QR

Wifi QR is a lazily-named project that automatically updates my guest wifi password on a set schedule. It then generates a QR code and displays it on an e-ink screen so that when my guests point their phone camera at the screen they are logged in to my guest network.

## Why though?

The real motivation for this project was "to see if I could", but if you're looking for a few benefits of a project like this, here's a few:

- Having a complicated password is a good thing because it makes it hard to guess
  - This is inconvenient for our wifi guests so we let a QR code log them in
- Changing a password frequently is generally considered a good practice because it prevents continued (possibly unauthorized) use
  - This is _also_ inconvenient which is why this project does it automatically

Hopefully even if you're not interested in making your own you can at least see why _I_ chose to make it. Assuming that is the case, let's see how it was done.

## Parts list

I needed **one** of the following:

- Raspberry Pi Zero
  - [Adafruit](https://www.adafruit.com/product/3400)
  - [Cytron](https://www.cytron.io/p-raspberry-pi-zero-w)
  - [ThePiHut](https://thepihut.com/products/raspberry-pi-zero-w)
- Raspberry Pi Zero with headers
  - [Adafruit](https://www.adafruit.com/product/3708)
- Raspberry Pi Zero 2
  - [Adafruit](https://www.adafruit.com/product/5291)
  - [CanaKit](https://www.canakit.com/raspberry-pi-zero-2-w.html)
  - [ThePiHut](https://thepihut.com/products/raspberry-pi-zero-2)
- Raspberry Pi Zero 2 with headers
  - [ThePiHut](https://thepihut.com/products/raspberry-pi-zero-2?variant=41181426942147)

Then I needed something to store stuff on because Raspberry Pi's don't have a hard / solid state drive:

- SD card
  - [Amazon](https://www.amazon.com/gp/product/B073K14CVB)

Next, the screen. I used an e-ink screen because they look nice and are low-power, but any screen compatible with the Raspberry Pi should suffice:

- Waveshare e-ink screen
  - [Amazon](https://www.amazon.com/Waveshare-4-2inch-Module-Three-Color-Communicating/dp/B075FRVC4L)
  - [Waveshare](https://www.waveshare.com/product/displays/e-paper/4.2inch-e-paper-module-c.htm)

Because my screen had connection cables included I didn't need to buy any. That said I did need GPIO headers for the Raspberry Pi:

- Raspberry Pi Zero GPIO headers
  - [Amazon](https://www.amazon.com/Break-Away-2x20-pin-Strip-Header-Raspberry/dp/B0756KM7CY)
- Rasberry Pi jumper cables
  - [Amazon](https://www.amazon.com/dp/B09FP2F22C)

## Raspberry Pi setup

With the parts in hand, I needed to set up the Raspberry Pi so that I could use it for anything. Then I'd need to tailor it for the needs of this project.

### Make it do anything

I always format SD cards before I use them in Raspberry Pi projects, so I started by connecting the card to my Windows machine and using the tool "diskpart" from the Command Prompt.

`diskpart`

[![image_not_found](/assets/images/diskpart.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/diskpart.png)

Within "diskpart", the first step was to find my SD card.

`list disk`

[![image_not_found](/assets/images/diskpart_list_disk.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/diskpart_list_disk.png)

Because I know my card is about 16 GB, I selected disk 1.

`select disk 1`

[![image_not_found](/assets/images/diskpart_select_disk.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/diskpart_select_disk.png)

After that I cleaned the disk.

`clean`

[![image_not_found](/assets/images/diskpart_clean.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/diskpart_clean.png)

Then I created the primary partition for later use.

`create partition primary`

[![image_not_found](/assets/images/diskpart_create_partition.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/diskpart_create_partition.png)

And last I formatted the drive.

`format fs=fat32`

[![image_not_found](/assets/images/diskpart_format.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/diskpart_format.png)

With the SD card prepped, I downloaded an image of Raspberry Pi OS compatible with my Raspberry Pi Zero.

[![image_not_found](/assets/images/raspi_os.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_os.png)

Then I used the Raspberry Pi Imager to burn the image on to the disk. The imager's interface is pretty nice and allows for very easy SSH and wifi configuration (shown in a sec).

[![image_not_found](/assets/images/raspi_imager.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_imager.png)

Within the "Advanced options" I enabled SSH and set my desired SSH username and password.

[![image_not_found](/assets/images/raspi_imager_ssh.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_imager_ssh.png)

Then I configured the wifi settings so that my Raspberry Pi would connect to my home network. I had it connect to my IoT VLAN (**not** the guest network). [My home network topology](https://github.com/kmanc/unifi_network_setup) is beyond the scope of this, but it was important not to have the Raspberry Pi connect to the network whose password it would be changing.

[![image_not_found](/assets/images/raspi_imager_wireless.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_imager_wireless.png)

Finally, I burned the image to the disk.

[![image_not_found](/assets/images/raspi_imager_write.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_imager_write.png)