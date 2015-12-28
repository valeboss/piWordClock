# -*- coding: utf-8 -*-
__author__ = 'Valentin'
from piwordclock import wordclock as wc
import time
import sys

if __name__ == '__main__':
    clock = wc.WordClock(15, 15)
    for each_arg in sys.argv:
        print(each_arg)
    while True:
        try:
            print("Übernommenes Argument: " + sys.argv[1])
            clock.run_clock(sys.argv[1])
        except (IndexError, KeyError):
            clock.run_clock("words")
        time.sleep(1)
