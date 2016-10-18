CHeap Arm Project - Teleoperation Control Software
==================================================
`HomePage <https://github.com/Mobile-CHAP>`_

This repository contains the source files for the CHeap Arm Project control software.

Installation
==================

The robot operates using a Flask (Python) powered webserver hosting a touchscreen compatible tele-operation system.
Live images are streamed from the web server, and commands are passed back from the client to a Python web socket listener for handling and transmission using USB2Dynamixel.
A Raspberry Pi or similiar is recommended for the project, with `DietPI <http://dietpi.com/>`_ being the preferred Linux distro (due to being mostly empty by default, with an effective setup system and SSH-ready on first boot, i.e. no HDMI or keyboard needed).

--------------------------------------------------------------------------------


1. Install `DietPi <http://dietpi.com/>`_ to an empty SD card, place in Raspberry Pi and power up.

Optional: Edit "dietpi.txt" file on SD card to enter WiFi name and password if using SSH.

2. Follow DietPi onscreen instructions to complete setup.

3. Download and compile `OpenCV 3 <http://opencv.org/downloads.html>`_.

Required binaries can be installed on Linux using the following command, Python modules such as numpy and scipy are best installed this way to avoid compiling on the Raspberry Pi::
	
	sudo apt-get install python-dev python-pip python-numpy python-scipy python-serial uwsgi uwsgi-plugin-python nginx


To correctly setup python please run the following commands/install the following libraries::

	pip install gevent autobahn[twisted] flask pypot

Using git::

	sudo apt-get install git
	
Clone this repository::

	git clone https://github.com/Mobile-CHAP/controller.git
	
Enter downloaded folder::

	cd controller
	
Run CHAP::

	python CHAP --help

Usage
=====
The 'CHAP' module can be run from the parent folder (folder containing the README and LICENSE files) using the following command::
	
	python CHAP --help

The response will list the available commands. Each sub-system (web_server,stream_server,control_listener) must be started for the system to fully work.
If devMode is set to 'true' within the settings file, the control_listener will not be used by the client and the control_listener will not connect to Dynamixels.

Modules must be run indivudally in any order using the start command::

	python CHAP --start web_server
	OR
	python CHAP -s web_server

The file 'settings.yml contains the following options:

.. code-block:: yaml
	:linenos:
	
	devMode: true 
	dynamixels: #IDs of all used dynamixels.
	release:
		serverIP: '192.168.42.1' #IP address of CHAP robot.
	dev:
		serverIP: '127.0.0.1' #For testing on local machine.

These can be adjusted based on whether or not development and testing is being done on a local machine while the control listener is not running (such as for HTML/JS development), or over an internet connection with fully CHAP systems in use.

Changes
=======

Changes to camera feed such as additional preprocessing or frame usage can be made in CHAP/CHAP_Controller/camera.py.
Client side JavaScript is managed in CHAP/CHAP_Controller/static/js/telecontroller.js
