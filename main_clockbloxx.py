import numpy as np
from neopixel import *
import time

from piwordclock import ClockBloxx as cb

# Begin strip and create bloxx_board
strip = Adafruit_NeoPixel((15 * 15), 18, 800000, 5, False, strip_type=ws.WS2811_STRIP_RGB)
strip.begin()

bloxx_board = cb.ClockBloxx(strip)


#%% Create ClockBloxx
vera_xy = np.array([[1,1], [1,2], [1,3], [2,2]])

t_element = cb.BloxxElement(vera_xy, rgb=None)
miniblock = cb.BloxxElement(xy=None, rgb=None)
miniblock = cb.BloxxElement(xy=None, rgb=None)

bloxx_board.add_bloxx(t_element)
bloxx_board.add_bloxx(miniblock)
bloxx_board.add_bloxx(miniblock)


#%% Show on clock
bloxx_board.render_bloxx_to_clock()


