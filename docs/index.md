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

### Make it control the screen

Having finished configuring a Raspberry Pi to connect to my home network and accept an SSH connection, I needed to prepare it to display a QR code to the e-ink screen. My first step was to solder the header pins to the board and figure out what pins on the screen had to connect to what pins on the board. [Waveshare's documentation](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module_Manual#Users_Guides_of_Raspberry_Pi) is pretty helpful in this regard; because my screen had the cables connected to the screen already all I had to do was put them on the corresponding header pin

[![image_not_found](/assets/images/waveshare_eink_pins.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/waveshare_eink_pins.png)

Next I had to install some packages and libraries, so I started by ensuring that the Raspberry Pi was up to date

`sudo apt update && sudo apt upgrade`

[![image_not_found](/assets/images/raspi_apt_update_and_upgrade.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_apt_update_and_upgrade.png)

Then I proceeded to install the packages.

`sudo apt install git libopenjp2-7 python3-pip`

[![image_not_found](/assets/images/raspi_installs.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_installs.png)

And finally I got the required broadcom library set up, starting with the download.

`wget https://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz`

[![image_not_found](/assets/images/raspi_broadcom_library.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_broadcom_library.png)

Then I unzipped the file.

`tar zxvf bcm2835-1.71.tar.gz`

[![image_not_found](/assets/images/raspi_broadcom_library_unzip.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_broadcom_library_unzip.png)

I changed my working directory to the newly created one.

`cd bcm2835-1.71/`

[![image_not_found](/assets/images/raspi_broadcom_library_directory.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_broadcom_library_directory.png)

Then I ran the configuration script within it.

`sudo ./configure`

[![image_not_found](/assets/images/raspi_broadcom_library_configure.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_broadcom_library_configure.png)

After that I had to run the make script.

`sudo make`

[![image_not_found](/assets/images/raspi_broadcom_library_make.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_broadcom_library_make.png)

Then check the make script's completion

`sudo make check`

[![image_not_found](/assets/images/raspi_broadcom_library_check.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_broadcom_library_check.png)

And finally install it, as everything had worked out fine.

`sudo make install`

[![image_not_found](/assets/images/raspi_broadcom_library_install.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_broadcom_library_install.png)

With most of the software in place, I had to ensure that SPI was enabled on the Raspberry Pi.

`sudo raspi-config`

I chose option 3 for interface.

[![image_not_found](/assets/images/raspi_config.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_config.png)

Then option I4 for SPI.

[![image_not_found](/assets/images/raspi_config_spi.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_config_spi.png)

I checked the box to enable the SPI interface.

[![image_not_found](/assets/images/raspi_config_spi_enable.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_config_spi_enable.png)

And finally closed the option menu.

[![image_not_found](/assets/images/raspi_config_finish.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_config_finish.png)

## Project setup

With the Raspberry Pi set up, I needed to write the code to actually do the wifi-and-qr-code stuff. I started by changing directories to my home directory.

`cd ~`

From there I made a directory and started working on some Python. For anyone following along with their own Raspberry Pi, cloning my repo from Github should do the trick.

`git clone https://github.com/kmanc/wifi_qr.git`

[![image_not_found](/assets/images/raspi_git_clone.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_git_clone.png)

My repo has two files from [Waveshare's Github repo](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd) that are specific to the board that I used. The `epdconfig.py` and `epd4in2.py` files are used to control my e-ink screen.

For anyone following along who has a Unifi-based home network, you're almost done! All that's left is to navigate to the project directory.

`cd wifi_qr`

[![image_not_found](/assets/images/raspi_wifi_qr_directory.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_wifi_qr_directory.png)

Then install the project requirements.

`python3 -m pip install -r requirements.txt`

[![image_not_found](/assets/images/raspi_wifi_qr_installs.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_wifi_qr_installs.png)

Change the `config.ini` file such that it matches your network.

`nano config.ini`

And set a cron schedule; I save my cron schedule in the `crontab` file within the project

`crontab -e`

[![image_not_found](/assets/images/raspi_crontab.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_crontab.png)

With the cron schedule that I use, every Monday morning at midnight (after any weekend guests have left) or every power cycle of the Raspberry Pi changes my guest wifi network's password and the corresponding QR code.

## How I developed the script

For the most part, the `update_wifi.py` script is pretty straightforward. It creates a password of the length specified in the config file, updates the guest network to use that password, makes a QR code with the password and network SSID, and then writes that to the screen. The "hardest" part was using Python to change the guest network's password, but not necessarily because that is difficult to do. The tricky part was knowing _what_ to do, so for that I turned to my web browser's dev tools. I opened up the dev tools and logged in to my home network's management portal, keeping track of the full request and any parameters required to log in.

[![image_not_found](/assets/images/network_devtools_login.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/network_devtools_login.png)

Then I used the management portal to manually change the guest network's password, again keeping note of the requests and parameters using dev tools.

[![image_not_found](/assets/images/network_change_password.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/network_devtools_change_password.png)

[![image_not_found](/assets/images/network_change_password_headers.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/network_devtools_change_password_headers.png)

[![image_not_found](/assets/images/network_change_password_payload.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/network_devtools_change_password_payload.png)

Armed with this information, I made a very simple Python client in `router_clients.py` that mimicked the same requests. By doing this, I'd be able to (mostly) keep the code in `update_wifi.py` the same if I ever changed network hardware, or if I wanted to add supported hardware for a friend. This is to say that other hardware _is supportable_, I just haven't built it
