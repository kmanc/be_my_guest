#!/bin/bash

# Change to home
cd /home/pi

# Update the Raspberry Pi
sudo apt update && sudo apt full-upgrade -y && sudo apt autoremove -y

# Add required packages
sudo apt install git libopenjp2-7 libusb-dev python3-pip -y

# Download Broadcom library
wget https://www.airspayce.com/mikem/bcm2835/bcm2835-1.71.tar.gz

# Unzip library
tar zxvf bcm2835-1.71.tar.gz

# Enter library directory
cd bcm2835-1.71/

# Run library config
sudo ./configure

# Build library
sudo make

# Run tests
sudo make check

# Install
sudo make install

# Change to home
cd /home/pi

# Enable SPI interface
sudo raspi-config nonint do_spi 0

# Clone be_my_guest
git clone https://github.com/kmanc/be_my_guest.git

# Enter the be_my_guest directory
cd be_my_guest

# Install the requirements
python3 -m pip install -r requirements.txt

# Change to home
cd /home/pi

# Add comment to cron file
echo "# min hour day(of month) mon day(of week) command" >> cronfile

# Add comment to cron file
echo "# This one should do every Monday at midnight" >> cronfile

# Add command to cron file
echo "0 0 * * MON python3 /home/pi/wifi_qr/update_wifi.py" >> cronfile

# Add comment to cron file
echo "# This one should do every reboot" >> cronfile

# Add command to cron file
echo "@reboot sleep 90 && python3 /home/pi/wifi_qr/update_wifi.py" >> cronfile

# Install the cron job
crontab cronfile

# Remove the no-longer-needed file
rm cronfile

# Restart the Raspberry Pi
sudo reboot now
