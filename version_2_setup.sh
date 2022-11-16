#!/bin/bash

# Change to home
cd /home/pi

# Update the Raspberry Pi
sudo apt update && sudo apt full-upgrade -y && sudo apt autoremove -y

# Add required packages
sudo apt install git libopenjp2-7 libusb-dev python3-pip uhubctl -y

# Allow uhubctl to run without sudo
sudo chmod u+s /usr/sbin/uhubctl

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

# Clone micronucleus
git clone https://github.com/micronucleus/micronucleus.git

# Enter commandline directory
cd micronucleus/commandline

# Build micronucleus
sudo make

# Move executable
sudo cp micronucleus /usr/local/bin

# Copy rules
sudo cp 49-micronucleus.rules /etc/udev/rules.d/

# Change to home
cd /home/pi

# Turn off the USB ports for a few seconds in the background
uhubctl -l 1-1 -a cycle -d 5 &

# Upgrade the firmware on the connected board
micronucleus --run micronucleus/firmware/upgrades/upgrade-t85_default.hex

# Download arduino-cli
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

# Move executable
sudo mv bin/arduino-cli /usr/local/bin

# Remove leftovers
rm -rf bin/

# Create arduino-cli config
arduino-cli config init

# Update arduino-cli config
sed -i 's+\[]+\[https://raw.githubusercontent.com/ArminJo/DigistumpArduino/master/package_digistump_index.json]+g' .arduino15/arduino-cli.yaml

# Reload arduino-cli config
arduino-cli core update-index

# Install required arduino-cli platform
arduino-cli core install digistump:avr

# Change to home
cd /home/pi

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
echo "0 0 * * MON python3 /home/pi/be_my_guest/update_wifi.py" >> cronfile

# Add comment to cron file
echo "# This one should do every reboot" >> cronfile

# Add command to cron file
echo "@reboot sleep 90 && python3 /home/pi/be_my_guest/update_wifi.py" >> cronfile

# Install the cron job
crontab cronfile

# Remove the no-longer-needed file
rm cronfile

# Restart the Raspberry Pi
sudo reboot now
