# -*- coding: utf-8 -*-

import time
import numpy as np
from neopixel import *


class ClockBloxx(object):

    def __init__(self, led_strip):
        self._led_strip = led_strip
        self._bloxx_elements = []

    def clear_clock(self):
        for i in range(self._led_strip.numPixels()):
            self._led_strip.setPixelColor(i, Color(0, 0, 0))

    def show_cleared_clock(self):
        self.clear_clock()
        self._led_strip.show()

    def add_bloxx(self, bloxx_element):
        self._bloxx_elements.append(bloxx_element)

    def render_bloxx_to_clock(self):
        strip_indexes = []
        strip_colors = []
        for element in self._bloxx_elements:
            new_strip_indexes = np.zeros(element.xy.shape[0])
            ind_odd = np.where(element.xy[:, 1] % 2 == 1)
            ind_even = np.where(element.xy[:, 1] % 2 == 0)
            new_strip_indexes[ind_even] = ((element.xy[ind_even, 1] + 1) * 15 - 1 - element.xy[ind_even, 0]).astype(np.uint32)
            new_strip_indexes[ind_odd] = (element.xy[ind_odd, 0] + element.xy[ind_odd, 1] * 15).astype(np.uint32)
            strip_indexes.extend(new_strip_indexes)
            for index in strip_indexes:
                strip_colors.append(element.rgb)
        self.clear_clock()
        for index in range(len(strip_indexes)):
            self._led_strip.setPixelColor(int(strip_indexes[index]), Color(*strip_colors[index].tolist()))
        self._led_strip.show()



class BloxxElement(object):

    def __init__(self, xy=None, rgb=None, name="BloxxElement"):
        self._name = name
        if xy is None:
            self.xy = np.random.random_integers(low=0, high=14, size=(1,2))
        else:
            self.xy = xy
        self.xy_0 = np.copy(xy)
        if rgb is None:
            self.rgb = np.random.random_integers(low=0, high=255, size=(3,)).astype(np.uint32)
        else:
            self.rgb = rgb.astype(dtype=np.uint32)
        self.rgb_0 = np.copy(self.rgb)

    def translate(self, trans_xy=None):
        if trans_xy is None:
            trans_xy = np.random.random_integers(low=0, high=14, size=(1,2))
        self.xy = np.add(self.xy, trans_xy)
