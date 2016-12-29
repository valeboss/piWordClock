# -*- coding: utf-8 -*-
__author__ = 'Valentin'

from tkinter import *
from piwordclock.pixel import Pixel

x_pixelsize = 30
y_pixelsize = 30
pixels = []

letters_on_front = "KXUIWOSEPLNEMTSLDAESÖLISTCVZUDEWESUSINDISTCNGÜZWANZIGFÜNFXRJMAVIERTELZEHNPÄDZWEIHALBZWÖLFILNACHTVOR" \
                   "YNACHWIZNEUNELFSECHSBXHALBDREINSÖKNEONEUHRACSIEBENDADREINSECHSELFAFHZEHNEUNVIERYPSZWEIACHTFÜNFKHJHC" \
                   "ZWÖLFÄUHRVBAHYKLAWIRTESNMPM"

def set_up_matrix(visibility):
    for y in range(0, 15):
        for x in range(0, 15):
            pixel = Pixel(visibility, x_pixelsize * x, y_pixelsize * y, "yellow", "white")
            pixels.append(pixel)

def draw_pixels(pixels, strip):
    # Hintergrund zeichnen
    strip.w.create_rectangle(0, 0, strip.canvas_width, strip.canvas_height, fill="grey", outline="grey")
    # Pixel zeichnen
    offset = 1
    for pixel in pixels:
        pixel_no = pixel.y * 15 + pixel.x
        y = int(pixel_no / 15)
        col = pixel_no % 15
        if y % 2 != 0:
            x = abs(col - 14)
        else:
            x = col
        if pixel.state:
            # print(str(pixel.x) + " " + str(pixel.y) + " " + str(pixel.colour))
            strip.w.create_rectangle(pixel.x + offset, pixel.y + offset, pixel.x + x_pixelsize - offset,
                                     pixel.y + y_pixelsize - offset, fill=pixel.colour_on, outline=pixel.colour_on)
            strip.w.create_text(pixel.x + offset + x_pixelsize / 2, pixel.y + offset + y_pixelsize / 2,
                                letters_on_front[y * 15 + x])
        else:
            strip.w.create_rectangle(pixel.x + offset, pixel.y + offset, pixel.x + x_pixelsize - offset,
                                     pixel.y + y_pixelsize - offset, fill=pixel.colour_off, outline=pixel.colour_off)
            strip.w.create_text(pixel.x + x_pixelsize / 2, pixel.y + y_pixelsize / 2, letters_on_front[y * 15 + x])


class Adafruit_NeoPixel(object):

    def __init__(self, pixel_count, i, j, k, l):
        self.pixel_count = pixel_count
        self.i = i
        self.j = j
        self.k = k
        self.l = l
        self.canvas_width = 450
        self.canvas_height = 450
        self.pixels = []
        self.master = Tk()
        self.w = Canvas(self.master, width=self.canvas_width, height=self.canvas_height)
        self.w.pack()
        self.offset = 5
        self.x_pixelsize = 30
        self.y_pixelsize = 30
        self.w.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill="grey", outline="grey")
        #self.w.mainloop()

    def begin(self):
        pass

    def setPixelColorRGB(self, pixel_no, r, g, b):
        y = int(pixel_no / 15)
        col = pixel_no % 15
        if y % 2 != 0:
            x = abs(col - 14)
        else:
            x = col
        factor = 1
        rgb = (r * factor, g * factor, b * factor)
        #self.w.create_rectangle(x * x_pixelsize + self.offset, y * y_pixelsize + self.offset,
        #                        x * x_pixelsize + self.x_pixelsize - self.offset,
        #                        y * y_pixelsize + self.y_pixelsize - self.offset,
        #                        fill=(self.rgb_to_hex(rgb)), outline=(self.rgb_to_hex(rgb)))
        self.w.create_text(x_pixelsize * (x + 0.5), y_pixelsize * (y + 0.5), text=letters_on_front[y * 15 + x],
                           font=('lucida', 14, 'bold'), fill=self.rgb_to_hex(rgb))#, outline=self.rgb_to_hex(rgb))

    def rgb_to_hex(self, rgb):
        return '#%02X%02X%02X' % rgb

    def show(self):
        self.w.update()


#strip = Adafruit_NeoPixel(225, 18, 80000, 5, False)
#strip.begin()
#set_up_matrix(False)
#draw_pixels(pixels, strip)
#strip.setPixelColorRGB(15, 200, 50, 1)
#mainloop()
