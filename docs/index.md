---
title: "Be My Guest"
---

# Be My Guest

"Be My Guest", named after [this catchy Simpsons tune](https://www.youtube.com/watch?v=TyWVaZsUQjc) is my solution to the annoyances connecting to my Guest Wifi. I felt I had to choose between:

- Having a complicated (i.e. more secure) password that is a pain for me to share and a worse pain for my guests to type
- Having a simple password that is easy to share and type, but also easily guessed

Either of these two options **also** suffered from two additional problems:

- Typing anything in to join my Guest Wifi is more effort than it has to be
- The password must either never change, or the effort of re-authenticating must be repeated now and then

"Be My Guest" solves all of the above issues by reducing the barrier to entry for my guests while maintaining my minimum bar for security. It:

- Changes my Guest Wifi password to a randomly-generated 30 character string every Monday morning
- Generates a QR code based on the current password that automatically logs a device in to my Guest Wifi
- [V2] Writes a program to a USB device that, when plugged in, types in the current password

As indicated above, I made two versions of "Be My Guest" based on the needs of my guests. Version 1 is best suited for environments that only have handheld mobile devices (phones, tablets, etc) join the Guest Wifi. Version 2 additionally supports devices that have USB ports (laptops, desktops, etc).

Version 1 | Version 2
--------- | ----
[![image_not_found](/assets/images/be_my_guest_v1_front.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/be_my_guest_v1_front.png) | [![image_not_found](/assets/images/be_my_guest_v2_front.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/be_my_guest_v2_front.png)
[![image_not_found](/assets/images/be_my_guest_v1_back.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/be_my_guest_v1_back.png) | [![image_not_found](/assets/images/be_my_guest_v2_back.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/be_my_guest_v2_back.png)


If you are interested in building your own version 1, check out [this guide](https://kmanc.github.io/be_my_guest/version_1.html)!
If instead you want to build version 2, check out [this guide](https://kmanc.github.io/be_my_guest/version_2.html).
If you're into stories and you want to see what went into building the two versions, head [over here](https://kmanc.github.io/be_my_guest/behind_the_scenes.html).










DELETE ME AND ANYTHING BELOW ME

Next I moved on to setting up `micronucleus` so that I could update the bootloader on my Digispark boards, and upload Arduino scripts to them.

`cd ~`

From my home directory I cloned the repo to my Raspberry Pi.

`git clone https://github.com/micronucleus/micronucleus.git`

[![image_not_found](/assets/images/raspi_micronucleus.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_micronucleus.png)

Then I changed into it's command line directory so I could build the executable.

`cd micronucleus/commandline/`

[![image_not_found](/assets/images/raspi_micronucleus_commandline.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_micronucleus_commandline.png)

After that I actually built the executable.

`make`

[![image_not_found](/assets/images/raspi_micronucleus_make.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_micronucleus_make.png)

And moved the file to a directory in my PATH so that I could run it more conveniently.

`sudo cp micronucleus /usr/local/bin`

[![image_not_found](/assets/images/raspi_micronucleus_bin.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_micronucleus_bin.png)

Before leaving the `micronucleus` directory, I copied a file provided by the project to help the Raspberry Pi identify boards running the `micronucleus` bootloader.

`sudo cp 49-micronucleus.rules /etc/udev/rules.d/`

[![image_not_found](/assets/images/raspi_micronucleus_rules.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_micronucleus_rules.png)

With that all done, I returned to my home directory.

`cd ~`

At this point, I upgraded the bootloader on the board I intended to use, as it shipped with a very old version.

`micronucleus --run micronucleus/firmware/upgrades/upgrade-t85_default.hex`

[![image_not_found](/assets/images/raspi_micronucleus_upgrade.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_micronucleus_upgrade.png)

Although I now could _upload_ Arduino scripts to my Digispark board, I had no way to _compile_ them, so I needed the `arduino-cli` tool. I downloaded and ran the installer first.

`curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh`

[![image_not_found](/assets/images/raspi_arduino_cli.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_arduino_cli.png)

Then I moved the executable to the same directory in my PATH that I had moved `micronucleus` into.

`sudo mv bin/arduino-cli /usr/local/bin`

[![image_not_found](/assets/images/raspi_arduino_cli_bin.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_arduino_cli_bin.png)

After that I deleted the leftover (now empty) directory that the installer had created.

`rm -rf bin/`

[![image_not_found](/assets/images/raspi_arduino_cli_cleanup.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_arduino_cli_cleanup.png)

Next I had to teach `arduino-cli` how to work with my Digispark board and `micronucleus`, starting by creating a config file.

`arduino-cli config init`

[![image_not_found](/assets/images/raspi_arduino_cli_config_init.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_arduino_cli_config_init.png)

I had to edit that config to include a specific package index for Digispark (https://raw.githubusercontent.com/ArminJo/DigistumpArduino/master/package_digistump_index.json).

`nano .arduino15/arduino-cli.yaml`

[![image_not_found](/assets/images/raspi_arduino_cli_config_change.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_arduino_cli_config_change.png)

Nearly done, I had `arduino-cli` reload the config to take any actions needed based on the new config file.

`arduino-cli core update-index`

[![image_not_found](/assets/images/raspi_arduino_cli_update.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_arduino_cli_update.png)

And finally with all that complete, I could install the proper platform for `arduino-cli` to compile for my Digispark board.

`arduino-cli core install digistump:avr`

[![image_not_found](/assets/images/raspi_arduino_cli_install.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/raspi_arduino_cli_install.png)








## How I developed the script

For the most part, the `update_wifi.py` script is pretty straightforward. It creates a password of the length specified in the config file, updates the guest network to use that password, makes a QR code with the password and network SSID, and then writes that to the screen. The "hardest" part was using Python to change the guest network's password, but not necessarily because that is difficult to do. The tricky part was knowing _what_ to do, so for that I turned to my web browser's dev tools. I opened up the dev tools and logged in to my home network's management portal, keeping track of the full request and any parameters required to log in.

[![image_not_found](/assets/images/network_devtools_login.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/network_devtools_login.png)

Then I used the management portal to manually change the guest network's password, again keeping note of the requests and parameters using dev tools.

[![image_not_found](/assets/images/network_devtools_change_password.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/network_devtools_change_password.png)

[![image_not_found](/assets/images/network_devtools_change_password_headers.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/network_devtools_change_password_headers.png)

[![image_not_found](/assets/images/network_devtools_change_password_payload.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/network_devtools_change_password_payload.png)

Armed with this information, I made a very simple Python client in `router_clients.py` that mimicked the same requests. By doing this, I'd be able to (mostly) keep the code in `update_wifi.py` the same if I ever changed network hardware, or if I wanted to add supported hardware for a friend. This is to say that other hardware _is supportable_, I just haven't built it
