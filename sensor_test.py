# -*- coding: utf-8 -*-
__author__ = 'Valentin'
from piwordclock import sensors
import time

if __name__ == '__main__':
    while True:
        print(sensors.read_adc(0))
        print(sensors.read_adc(1))
        print(sensors.read_adc(2))
        print(sensors.read_adc(3))
        print(sensors.read_adc(4))
        print(sensors.read_adc(5))
        print(sensors.read_adc(6))
        print(sensors.read_adc(7))
        print("##########")
        print(sensors.read_temp())
        print("##########")
        time.sleep(5)
