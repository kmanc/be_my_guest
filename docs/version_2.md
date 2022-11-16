---
title: "Be My Guest Version 2"
---

# Version 2

## Parts list

**One** of the following to be the base that gets built off of:

- Raspberry Pi B+
  - [Adafruit](https://www.adafruit.com/product/1914)
- Raspberry Pi 2B
  - [CanaKit](https://www.canakit.com/raspberry-pi-2.html)
- Raspberry Pi 3B
  - [CanaKit](https://www.canakit.com/raspberry-pi-3-model-b.html)
- Raspberry Pi 3B+
  - [Adafruit](https://www.adafruit.com/product/3775)
  - [ThePiHut](https://thepihut.com/products/raspberry-pi-3-model-b-plus)
- Raspberry Pi 4B
  - [Adafruit](https://www.adafruit.com/product/4295)
  - [ThePiHut](https://thepihut.com/products/raspberry-pi-4-model-b)
  - [CanaKit](https://www.canakit.com/raspberry-pi-4.html)

A "brain" for the base:

- SD card
  - [Amazon](https://www.amazon.com/gp/product/B073K14CVB)

A screen for the QR code. I used an e-ink screen because they look nice and are low-power, but any screen compatible with the Raspberry Pi should suffice:

- Waveshare e-ink screen
  - [Amazon](https://www.amazon.com/Waveshare-4-2inch-Module-Three-Color-Communicating/dp/B075FRVC4L)
  - [Waveshare](https://www.waveshare.com/product/displays/e-paper/4.2inch-e-paper-module-c.htm)

A USB device that can be programmed to automatically type in passwords

- Digispark ATTINY85
  - [Amazon](https://www.amazon.com/ACEIRMC-Digispark-Kickstarter-Attiny85-Development/dp/B08JGL5TSV/)

Possibly cables and headers. I did need GPIO headers for the Raspberry Pi, but my screen came with jumper cables so I didn't need those:

- Raspberry Pi Zero GPIO headers
  - [Amazon](https://www.amazon.com/Break-Away-2x20-pin-Strip-Header-Raspberry/dp/B0756KM7CY)
- Rasberry Pi jumper cables
  - [Amazon](https://www.amazon.com/dp/B09FP2F22C)

## Raspberry Pi setup

Raspberry Pis, though awesome, require a bit of setup before use

### Baseline setup

From a Windows machine, open a Command Prompt and type `diskpart` to use the diskpart tool.

`diskpart`

[![image_not_found](/assets/images/diskpart.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/diskpart.png)

List the disks connected to the machine.

`list disk`

[![image_not_found](/assets/images/diskpart_list_disk.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/diskpart_list_disk.png)

Choose the disk that you intend to write the Raspberry Pi Operating System (OS) to.

`select disk 1`

[![image_not_found](/assets/images/diskpart_select_disk.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/diskpart_select_disk.png)

Clean the disk.

`clean`

[![image_not_found](/assets/images/diskpart_clean.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/diskpart_clean.png)

Create a primary partition that can be formatted and written to.

`create partition primary`

[![image_not_found](/assets/images/diskpart_create_partition.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/diskpart_create_partition.png)

Format the drive with a FAT32 filesystem.

`format fs=fat32 quick`

[![image_not_found](/assets/images/diskpart_format.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/diskpart_format.png)

Download and use the Raspberry Pi Imager to burn the image on to the disk. The imager's interface is pretty nice and allows for very easy SSH and wifi configuration (shown in a sec).

[![image_not_found](/assets/images/raspi_imager.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_imager.png)

Within the "Advanced options" enable SSH and set the desired SSH username and password.

[![image_not_found](/assets/images/raspi_imager_ssh.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_imager_ssh.png)

Configure the Wifi settings so that the Raspberry Pi connects to the desired network. I had it connect to my IoT VLAN (**not** the guest network). [My home network topology](https://github.com/kmanc/unifi_network_setup) is beyond the scope of this guide, but it is important not to have the Raspberry Pi connect to the network whose password it will be changing.

[![image_not_found](/assets/images/raspi_imager_wireless.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_imager_wireless.png)

Finally, burn the image to the disk.

[![image_not_found](/assets/images/raspi_imager_write.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_imager_write.png)

NOTE: when you first boot the Raspberry Pi you may find that SSH is unstable. If that is the case it could be because of some flags set in the packets being sent and the way they interacted with your network; I was able to fix it by running the following command, substituting in the IP address of my Raspberry Pi.

`ssh pi@pis.ip.add.res 'echo "IPQoS cs0 cs0" | sudo tee -a /etc/ssh/sshd_config && sudo reboot now'`

### Super shortcut

You can run the following command which will complete all the steps for the sections below, or you can follow along with the sections below. 

NOTE: Plug in the Digispark device before running this command.
NOTE: You'll need to fill out your `config.ini` file either way (the very last step at the bottom).

`curl --proto "=https" --tlsv1.2 -sSf https://raw.githubusercontent.com/kmanc/be_my_guest/main/version_2_setup.sh | sh`

### Make it control the screen

To control the screen you will have to physically connect the screen to the Raspberry Pi. Mileage may vary depending on device, but [Waveshare's documentation](https://www.waveshare.com/wiki/4.2inch_e-Paper_Module_Manual#Users_Guides_of_Raspberry_Pi) gave a pretty good overview of the connections required.

[![image_not_found](/assets/images/waveshare_eink_pins.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/waveshare_eink_pins.png)

Before installing any new packages, ensure that your Operating System is up-to-date. Connect to the Raspberry Pi and update it.

`sudo apt update && sudo apt upgrade`

[![image_not_found](/assets/images/raspi_apt_update_and_upgrade.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_apt_update_and_upgrade.png)

Install required packages. If using a different screen you may have different dependencies.

`sudo apt install git libopenjp2-7 libusb-dev python3-pip`

[![image_not_found](/assets/images/raspi_v1_installs.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_v1_installs.png)

Download and install any additional software. In the case of the Waveshare e-ink screen, a Broadcom library is required.

`wget https://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz`

[![image_not_found](/assets/images/raspi_broadcom_library.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_broadcom_library.png)

Unzip the download.

`tar zxvf bcm2835-1.71.tar.gz`

[![image_not_found](/assets/images/raspi_broadcom_library_unzip.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_broadcom_library_unzip.png)

Change your working directory to the unzipped folder.

`cd bcm2835-1.71/`

[![image_not_found](/assets/images/raspi_broadcom_library_directory.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_broadcom_library_directory.png)

Run its configuration.

`sudo ./configure`

[![image_not_found](/assets/images/raspi_broadcom_library_configure.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_broadcom_library_configure.png)

Run the "make" script.

`sudo make`

[![image_not_found](/assets/images/raspi_broadcom_library_make.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_broadcom_library_make.png)

Check the "make" script's completion.

`sudo make check`

[![image_not_found](/assets/images/raspi_broadcom_library_check.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_broadcom_library_check.png)

Assuming the check passes, install the library.

`sudo make install`

[![image_not_found](/assets/images/raspi_broadcom_library_install.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_broadcom_library_install.png)

Open the Raspberry Pi's configuration menu to enable the SPI interface.

`sudo raspi-config`

Choose option 3.

[![image_not_found](/assets/images/raspi_config.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_config.png)

Then option I4 for SPI.

[![image_not_found](/assets/images/raspi_config_spi.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_config_spi.png)

Check the box to enable the SPI interface.

[![image_not_found](/assets/images/raspi_config_spi_enable.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_config_spi_enable.png)

Close the option menu.

[![image_not_found](/assets/images/raspi_config_finish.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_config_finish.png)

### Arduino CLI Setup

Move back to the home directory.

`cd ~`

Download and run the `arduino-cli` installer.

`curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh`

[![image_not_found](/assets/images/raspi_arduino_cli.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_arduino_cli.png)

Move the executable to a location within your PATH.

`sudo mv bin/arduino-cli /usr/local/bin`

[![image_not_found](/assets/images/raspi_arduino_cli_bin.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_arduino_cli_bin.png)

Delete "leftover" files and directories.

`rm -rf bin/`

[![image_not_found](/assets/images/raspi_arduino_cli_cleanup.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_arduino_cli_cleanup.png)

Create an arduino config file.

`arduino-cli config init`

[![image_not_found](/assets/images/raspi_arduino_cli_config_init.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_arduino_cli_config_init.png)

Edit the config to include a specific package index for Digispark (https://raw.githubusercontent.com/ArminJo/DigistumpArduino/master/package_digistump_index.json).

`nano .arduino15/arduino-cli.yaml`

[![image_not_found](/assets/images/raspi_arduino_cli_config_change.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_arduino_cli_config_change.png)

Reload the config to take any actions needed based on the new config file.

`arduino-cli core update-index`

[![image_not_found](/assets/images/raspi_arduino_cli_update.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_arduino_cli_update.png)

Install the proper platform for `arduino-cli` to compile for the Digispark board.

`arduino-cli core install digistump:avr`

[![image_not_found](/assets/images/raspi_arduino_cli_install.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_arduino_cli_install.png)

### Micronucleus Setup

Move back to the home directory.

`cd ~`

Cloned the repo to the Raspberry Pi.

`git clone https://github.com/micronucleus/micronucleus.git`

[![image_not_found](/assets/images/raspi_micronucleus.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_micronucleus.png)

Move to the `commandline` directory within `micronucleus`.

`cd micronucleus/commandline/`

[![image_not_found](/assets/images/raspi_micronucleus_commandline.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_micronucleus_commandline.png)

Build the executable.

`make`

[![image_not_found](/assets/images/raspi_micronucleus_make.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_micronucleus_make.png)

Move the executable to a location within your PATH.

`sudo cp micronucleus /usr/local/bin`

[![image_not_found](/assets/images/raspi_micronucleus_bin.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_micronucleus_bin.png)

Copy the `micronucleus.rules` file to the Raspberry Pi's `rules.d` directory

`sudo cp 49-micronucleus.rules /etc/udev/rules.d/`

[![image_not_found](/assets/images/raspi_micronucleus_rules.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_micronucleus_rules.png)

Move back to the home directory.

`cd ~`

Upgrade the bootloader on the board if it is an old version (which is very likely).

`micronucleus --run micronucleus/firmware/upgrades/upgrade-t85_default.hex`

[![image_not_found](/assets/images/raspi_micronucleus_upgrade.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_micronucleus_upgrade.png)

### Be My Guest Setup

Clone the "Be My Guest" repo to your Raspberry Pi.

`git clone https://github.com/kmanc/be_my_guest.git`

[![image_not_found](/assets/images/raspi_git_clone.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_git_clone.png)

NOTE: my repo has two files from [Waveshare's Github repo](https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd) that are specific to the board that I used. The `epdconfig.py` and `epd4in2.py` files are used to control my e-ink screen. You may need different files based on your screen.

Navigate to the `be_my_guest` directory.

`cd be_my_guest`

Set a cron schedule; I save my cron schedule in the `crontab` file within the project, so feel free to use that.

`crontab -e`

[![image_not_found](/assets/images/raspi_v1_crontab.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_v1_crontab.png)

Install the project requirements (optionally in a virtual environment - not shown).

`python3 -m pip install -r requirements.txt`

[![image_not_found](/assets/images/raspi_be_my_guest_installs.png)](https://raw.githubusercontent.com/kmanc/be_my_guest/main/docs/assets/images/raspi_be_my_guest_installs.png)

Change the `config.ini` file such that it matches your network.

`nano config.ini`