---
title: "Be My Guest"
---

# Be My Guest

"Be My Guest", named after [this catchy Simpsons tune](https://www.youtube.com/watch?v=TyWVaZsUQjc), is my solution to the annoyances connecting to my Guest wifi. I felt I had to choose between:

- Having a complicated (i.e. more secure) password that is a pain for me to share and a worse pain for my guests to type
- Having a simple password that is easy to share and type, but also easily guessed

Either of these two options **also** suffered from two additional problems:

- Typing anything in to join my Guest wifi is more effort than it has to be
- The password must either never change, or the effort of re-authenticating must be repeated now and then

"Be My Guest" solves all of the above issues by reducing the barrier to entry for my guests while maintaining my minimum bar for security. It:

- Changes my Guest wifi password to a randomly-generated 30 character string every Monday morning
- Generates a QR code based on the current password that automatically logs a device in to my Guest wifi
- [V2] Writes a program to a USB device that, when plugged in, types in the current password

As indicated above, I made two versions of "Be My Guest" based on the needs of my guests. Version 1 is best suited for environments that only have handheld mobile devices (phones, tablets, etc) join the Guest wifi. Version 2 additionally supports devices that have USB ports (laptops, desktops, etc).

Version 1 | Version 2
--------- | ----
[![image_not_found](/assets/images/be_my_guest_v1_front.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/be_my_guest_v1_front.png) | [![image_not_found](/assets/images/be_my_guest_v2_front.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/be_my_guest_v2_front.png)
[![image_not_found](/assets/images/be_my_guest_v1_back.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/be_my_guest_v1_back.png) | [![image_not_found](/assets/images/be_my_guest_v2_back.png)](https://raw.githubusercontent.com/kmanc/wifi_qr/main/docs/assets/images/be_my_guest_v2_back.png)


If you are interested in building your own version 1, check out [this guide](https://kmanc.github.io/be_my_guest/version_1.html)!

If instead you want to build version 2, check out [this guide](https://kmanc.github.io/be_my_guest/version_2.html).

If you're into stories and you want to see what went into building the two versions, head [over here](https://kmanc.github.io/be_my_guest/behind_the_scenes.html).
