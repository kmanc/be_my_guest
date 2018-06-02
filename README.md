# What is this

This is my solution to a problem that I (and maybe you) have: letting your friends
use your wifi when they come to visit sucks. 

### You have a few sucky options:
* Have a crappy password that you share with your friends
    * PRO - makes it easy for your friends to connect
    * CON - typically means your password is guessable/susceptible to
    brute-force-style attacks
    * CON - your password doesn't change (or at least doesn't change much),
    so over time you might not know who has access to your precious wifis
* Have a complicated password that you share with your friends
    * PRO - password probably isn't guessable/brute-forcible 
    * CON - it is most likely a pain to share that password
    * your password still probably doesn't change often, so once it is
    shared, it is shared for good
* Rotate your (either strong or weak) password often
    * PRO - password is probably pretty safe because the amount of time it stays
    valid is pretty small
    * CON - you have to reshare your password with friends often
    * CON - you also have to actually change the password often
    
### My solution
A raspberry pi, a wifi dongle, an LCD screen, and cron
* The raspberry pi + wifi dongle can log into your wifi with your password
* The raspberry pi can log into your router with _ITS_ password and change
the password to your wifi, and also save that password
* The raspberry pi + LCD screen can display a QR code that represents your wifi
password
* Cron allows you to set and forget the solution to do its work as often as you
would like

A really cool feature in IOS 11 is that the iPhone camera will recognize QR
codes by default, and prompt the user to take action. This means iPhone users
don't even need to download an app to read the QR code (_cough Android pls_)

Personally, I set mine to change the wifi password at 2:00am on the first of
every month. I find this to be a reasonable amount of time for a person to have
access without needing to rescan the QR code

For more on how I built this project, and how you can do it to, check out
[the full documentation here](https://kmanc.github.io/wifi_qr/)