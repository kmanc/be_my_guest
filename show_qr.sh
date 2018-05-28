#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
sudo fbi -T 1 --noverbose -a $DIR/wifi_qr.png
