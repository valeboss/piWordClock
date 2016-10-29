#!/bin/bash

sudo apt-get update && sudo apt-get upgrade
sudo apt-get install git scons swig build-essential python3 python3-dev
git clone https://github.com/jgarff/rpi_ws281x
cd rpi_ws281x
scons
cd python
sudo python3 setup.py install
cd ../
git clone https://github.com/tornadoweb/tornado.git
cd tornado
python setup.py build
sudo python3 setup.py install
cd ../
git clone https://github.com/valeboss/piWordClock.git
cd piWordClock
sudo python3 piwordclock.py
