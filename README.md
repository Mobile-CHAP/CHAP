# CHeap Arm Project
[HomePage](https://mobile-chap.github.io/Web/)

This repository contains the source files for the CHeap Arm Project, including the CAD files and tele-operation software.

# Hardware
[To-Do List](/design/ToDo.md)

All hardware related files can be found in the "design" folder. Full schematics are still to come. Latest editable files are all in the FreeCad format and hence FreeCad is required for usage: [FreeCad](http://www.freecadweb.org/).

# Software

The robot operates using a Flask (Python) powered webserver hosting a touchscreen compatible tele-operation system.
Live images are streamed from the web server, and commands are passed back from the client to a Python web socket listener for handling and transmission using USB2Dynamixel.

---

Latest versions of Python 2.7 and OpenCV 3 are both needed for the software to operate.

[Python 2.7](https://www.python.org/downloads/)

[OpenCV](http://opencv.org/downloads.html)

---

To correctly setup python please run the following commands/install the following libraries:
```
pip install gevent flask numpy serial
```

---
A Raspberry Pi or similiar is recommended for the project, with [DietPI](http://dietpi.com/) being the preferred Linux distro (due to being mostly empty by default, with an effective setup system and SSH-ready on first boot, i.e. no HDMI or keyboard needed).

# Credits
- USB2Dynamixel communication using [Python library by Phil Williammee](https://github.com/philwilliammee/dynamixel_simple_as_RPI)
