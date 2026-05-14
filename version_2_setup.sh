#!/bin/bash

# Change to home
cd /home/pi

# Update the Raspberry Pi
sudo apt update && sudo apt full-upgrade -y && sudo apt autoremove -y

# Add required packages
sudo apt install git libopenjp2-7 libusb-dev python3-pip -y

# Download lgpio repo
wget https://github.com/joan2937/lg/archive/master.zip

# Unzip repo
tar zxvf master.zip

# Enter repo directory
cd lg-master

# Run library installer
sudo make install

# Load the system package
sudo ldconfig

# Change to home
cd /home/pi

# Download Broadcom library
wget https://www.airspayce.com/mikem/bcm2835/bcm2835-1.77.tar.gz

# Unzip library
tar zxvf bcm2835-1.77.tar.gz

# Enter library directory
cd bcm2835-1.77/

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

# Create a persistent mountpoint for the Trinkey
sudo mkdir -p /media/CIRCUITPY

# Make sure it is owned by pi
sudo chown pi:pi /media/CIRCUITPY

# Configure the USB mount location and permissions
echo "LABEL=CIRCUITPY /media/CIRCUITPY vfat user,rw,umask=000,uid=1000,gid=1000,nofail,x-systemd.automount 0 0" | sudo tee /etc/fstab

# Clone be_my_guest
git clone https://github.com/kmanc/be_my_guest.git

# Enter the be_my_guest directory
cd be_my_guest

# Create a virtual environment with system packages available to it
python3 -m venv --system-site-packages venv

# Activate the virtual environment
source venv/bin/activate

# Install the requirements
pip install -r requirements.txt

# Change to home
cd /home/pi

# Add comment to cron file
echo "# min hour day(of month) mon day(of week) command" >> cronfile

# Add comment to cron file
echo "# This one should do every Monday at midnight" >> cronfile

# Add command to cron file
echo "0 0 * * MON /home/pi/be_my_guest/venv/bin/python /home/pi/be_my_guest/update_wifi.py" >> cronfile

# Add comment to cron file
echo "# This one should do every reboot" >> cronfile

# Add command to cron file
echo "@reboot sleep 90 && /home/pi/be_my_guest/venv/bin/python /home/pi/be_my_guest/update_wifi.py" >> cronfile

# Install the cron job
crontab cronfile

# Remove the no-longer-needed file
rm cronfile

# Restart the Raspberry Pi
sudo reboot now
