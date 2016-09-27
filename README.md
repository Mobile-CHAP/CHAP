# CHeap Arm Project - Teleoperation Control Software
[HomePage](https://mobile-chap.github.io/Web/)

This repository contains the source files for the CHeap Arm Project, including the CAD files and tele-operation software.

## Installation

The robot operates using a Flask (Python) powered webserver hosting a touchscreen compatible tele-operation system.
Live images are streamed from the web server, and commands are passed back from the client to a Python web socket listener for handling and transmission using USB2Dynamixel.

---

Latest versions of Python 2.7 and OpenCV 3 are both needed for the software to operate.

[OpenCV](http://opencv.org/downloads.html)

```
sudo apt-get install python-dev python-pip python-numpy python-scipy python-serial uwsgi uwsgi-plugin-python nginx
```

---

To correctly setup python please run the following commands/install the following libraries:
```
pip install gevent autobhan[twisted] flask pypot
```

---
A Raspberry Pi or similiar is recommended for the project, with [DietPI](http://dietpi.com/) being the preferred Linux distro (due to being mostly empty by default, with an effective setup system and SSH-ready on first boot, i.e. no HDMI or keyboard needed).


## Usage
The file 'settings.yml contains the following options:
```yaml
devMode: true #Switch IP addresses and disable websocket connections - for use during local testing without CHAP.
dynamixels: #IDs of all used dynamixels.
	...
release:
    serverIP: '192.168.42.1' #IP address of CHAP robot (won't change if using CHAP ad-hoc network).
dev:
    serverIP: '127.0.0.1' #IP address used during testing on local machine.
```
These can be adjusted based on whether or not development and testing is being done on a local machine with the control listener not running (such as for HTML/JS development), or over and internet connection with fully CHAP systems in use.


## Credits
- USB2Dynamixel communication using [Python library by Phil Williammee](https://github.com/philwilliammee/dynamixel_simple_as_RPI)
