#!/bin/bash
sudo fbi -T 1 --noverbose -a wifi_qr.png
sudo systemctl restart networking.service
