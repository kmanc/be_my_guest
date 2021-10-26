#!/bin/sh
cd ~/wifi_qr
/usr/bin/python3 password_and_qr_generate.py && /usr/bin/python3 network_update.py && /usr/bin/python3 display_update.py
