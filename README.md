# Eatventure-Bot

## About
This bot is designed to play Eatventure for you!
At the moment it can upgrade stations, complete upgrades in the upgrades menu and collect crates.

## Instructions

### To start the bot
To run the bot type the following command: `python3 main.py` and it will connect to your phone and start playing.
If the bot seems to be running but not doing anything, try restarting the VNC server on your phone (trust me).

### To control the bot (GUI coming soon...)
To pause the bot press: `f7`.
To unpause the bot press: `f9`.
To stop the bot press: `ctrl+c` in your terminal where it is running.

## Installation

### On your PC
To install the bot clone the repo and open a terminal inside of the newly cloned repo.
Install the requirements with: `pip install -r reqirements.txt`.


### Next, on your phone
To allow the bot to connect to your phone you need to download a VNC server on your phone.

#### Android
On Android I would recommend using DroidVNC: [Find it here](https://play.google.com/store/apps/details?id=net.christianbeier.droidvnc_ng&hl=en_US&pli=1)

#### IOS
I have not tested it on IOS so if you have a Apple phone feel free to update this readme.
I would try downloading a VNC server like Android and following their instuctions.

Then you will probably need to allow the app permissions on your phone by following the instructions they give you.

### Connecting your phone to your PC
1. At this stage, check your VNC server on your phone and find its IP address.
2. Open `data.py` in the bot directory and replace the value for `PHONE_IP_ADDRESS` with your phone's IP address.
3. Feel free to tinker with `data.py` to make it work with your phone size

### Now follow [instructions](#instructions)