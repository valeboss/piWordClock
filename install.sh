#!/bin/bash

sudo apt-get update && sudo apt-get upgrade
sudo apt-get install git scons swig build-essential python3 python3-dev
mkdir -r Programme
git clone https://github.com/jgarff/rpi_ws281x ~/Programme/
cd rpi_ws281x
scons
cd python
sudo python3 setup.py install
git clone https://github.com/tornadoweb/tornado.git ~/Programme/
cd ~/Programe/tornado
python3 setup.py build
sudo python3 setup.py install
git clone https://github.com/valeboss/piWordClock.git ~/Programme/
cd ~/Programme/piWordClock
sudo python3 piwordclock.py
