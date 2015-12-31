# -*- coding: utf-8 -*-
__author__ = 'Valentin'
import glob
import time
import math
try:
    import RPi.GPIO as GPIO
except ImportError:
    pass
from .matrix import Matrix
from .number import Number
#from .letterstring import Letterstring
try:
    from neopixel import *
except ImportError:
    from .wordclock_canvas import Adafruit_NeoPixel

## Die Klasse WordClock initalisiert ein Objekt für die Wortuhr.
#
# Steuert das Verhalten der Uhr.
class WordClock(object):
    """WordClock object utilises, controls and holds all information about the WordClock"""
    ## Initialisierungsfunktion der Klasse WordClock.
    #
    # @param self Object pointer
    # @param count_x Anzahl der Pixel in horizontaler Richtung (x-Achse).
    # @param count_y Anzahl der Pixel in vertikaler Richtung (y-Achse).
    def __init__(self, count_x, count_y):
        """Initializes the class WordClock."""
        # Wird alles nur gemacht, wenn sich das Programm auf dem RaspberryPi befindet.
        try:
            # Choose pinmode
            GPIO.setmode(GPIO.BCM)
            # Set up pim 24 as input with pull up resistance
            GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            # Sets up the sensor for temperature
            self.base_dir = '/sys/bus/w1/devices/'
            self.device_folder = glob.glob(self.base_dir + '28*')[0]
            self.device_file = self.device_folder + '/w1_slave'
        except NameError:
            pass
        # Initializes the Adafruit_NeoPixel library.
        self.strip = Adafruit_NeoPixel((count_x * count_y) + 3, 18, 800000, 5, False)
        self.strip.begin()
        # Initilaizes the matrix for the WordClock
        self.matrix = Matrix((count_x * count_y) + 3, self.strip)

    ## Diese Funktion startet die WordClock.
    #
    # @param self Object pointer
    # @param mode String der den Zeitmodus beschreibt. "words" für Wortmodus und "digital" für digitalen Modus.
    def run_clock(self, mode, optional_argument=None):
        token_dict = {"words": self.display_time_in_words,
                      "digital": self.display_digital_time_mode,
                      "temp": self.display_temperature,
                      "render_pixel_list": self.display_custom_pixel_list}
        self.matrix.clear_all_pixels()
        function_to_call = token_dict[mode]
        if not optional_argument:
            function_to_call(self.matrix)
        elif mode == "render_pixel_list":
            function_to_call(self.matrix, optional_argument)
        else:
            print("No match. Use words, digital, temp or pixel_list. See documentation for reference.")
            pass

    ## Diese Funktion stellt die aktuelle Zeit in Worten dar.
    #
    # @param self Object pointer
    # @param matrix Objekt der Klasse Matrix, welches die Matrix enthält, die die Zeit in Wörtern anzeigen soll.
    def display_time_in_words(self, matrix):
        datetime = time.localtime()
        hours = datetime[3]
        minutes = datetime[4]
        seconds = datetime[5]

        #minute_step = int((minutes+int(seconds/60))+2.5-((minutes+int(seconds/60))+2.5) % 5)
        if minutes % 10 >= 5:
            minute_step = minutes - (minutes % 10) + 5
        else:
            minute_step = minutes - (minutes % 10)

        minutes_binary = int(math.fabs(minutes - minute_step))

        hour_step = hours
        if minute_step >= 25:
            hour_step += 1

        if hour_step >= 12:
            hour_step -= 12
            pm = True
        else:
            pm = False

        # Displays "ES IST"
        visible_pixels = [18, 19, 22, 23, 24]

        # Displays "UHR"
        if minute_step == 0:
            visible_pixels.extend([204, 205, 206])

        # Binär kodierte Minutenanzeige auf den drei letzten LEDs; invertierte LEDs, da gerade Reihe
        binary_pixels = [[], [227], [226], [226, 227], [225]]
        visible_pixels.extend(binary_pixels[minutes_binary])

        #if minutes_binary == 1:
        #    visible_pixels.extend([227])
        #elif minutes_binary == 2:
        #    visible_pixels.extend([226])
        #elif minutes_binary == 3:
        #    visible_pixels.extend([226, 227])
        #elif minutes_binary == 4:
        #    visible_pixels.extend([225])

        if minute_step == 5 or minute_step == 25 or minute_step == 35 or minute_step == 55:
            visible_pixels.extend([53, 54, 55, 56])
        if minute_step == 25 or minute_step == 40 or minute_step == 45 or minute_step == 50 or minute_step == 55:
            visible_pixels.extend([96, 97, 98])
        if minute_step == 5 or minute_step == 10 or minute_step == 15 or minute_step == 20 or minute_step == 35:
            visible_pixels.extend([100, 101, 102, 103])
        if minute_step == 15 or minute_step == 45:
            visible_pixels.extend([62, 63, 64, 65, 66, 67, 68])
        if minute_step == 30:
            visible_pixels.extend([80, 81, 82, 83])
        if minute_step == 25 or minute_step == 35:
            visible_pixels.extend([121, 122, 123, 124])
        if minute_step == 20 or minute_step == 40:
            visible_pixels.extend([46, 47, 48, 49, 50, 51, 52])
        if minute_step == 10 or minute_step == 50:
            visible_pixels.extend([69, 70, 71, 72])

        if hour_step == 1:
            if minute_step != 0:
                visible_pixels.extend([153, 154, 155, 156])
            else:
                visible_pixels.extend([153, 154, 155])
        elif hour_step == 2:
            visible_pixels.extend([181, 182, 183, 184])
        elif hour_step == 3:
            visible_pixels.extend([151, 152, 153, 154])
        elif hour_step == 4:
            visible_pixels.extend([174, 175, 176, 177])
        elif hour_step == 5:
            visible_pixels.extend([189, 190, 191, 192])
        elif hour_step == 6:
            visible_pixels.extend([156, 157, 158, 159, 160])
        elif hour_step == 7:
            visible_pixels.extend([143, 144, 145, 146, 147, 148])
        elif hour_step == 8:
            visible_pixels.extend([185, 186, 187, 188])
        elif hour_step == 9:
            visible_pixels.extend([170, 171, 172, 173])
        elif hour_step == 10:
            visible_pixels.extend([167, 168, 169, 170])
        elif hour_step == 11:
            visible_pixels.extend([161, 162, 163])
        elif hour_step == 12 or hour_step == 0:
            visible_pixels.extend([198, 199, 200, 201, 202])
        else:
            print("Dies hätte nicht passieren dürfen; Fehler in Funktion: display_time_in_words")
            return

        for i in visible_pixels:
            matrix.pixels[i].state = True

        matrix.draw_pixels()

    ## Diese Funktion zeigt die aktuelle Temperatur in °C auf der WordClock an.
    #
    # @param self Object pointer
    # @param matrix Objekt der Klasse Matrix, welches die Matrix enthält, die die Temperatur anzeigen soll.
    def display_temperature(self, matrix):
        temp = float(self.read_temp()[0])
        temp_ones = temp % 10
        temp_tens = (temp - temp_ones) * 0.1
        #print(temp, temp_tens, temp_ones)

        t_o = Number(6, 0, int(round(temp_ones, 0)))
        t_t = Number(0, 0, int(round(temp_tens, 0)))

        deg_c_pixels = [1, 2, 10, 13, 15, 16, 17, 21, 22, 24, 28, 34, 44, 54, 64, 68, 75, 76, 77]
        offset = 110
        for i in deg_c_pixels:
            position = i + (i//10)*5 + offset
            matrix.pixels[position].set_state(True)

        for i in t_o.visible_pixels:
            offset = t_o.y * 15 + t_o.x
            matrix.pixels[i + offset].set_state(True)

        for i in t_t.visible_pixels:
            offset = t_t.y * 15 + t_t.x
            matrix.pixels[i + offset].set_state(True)

        matrix.draw_pixels()

    ## Diese Funktion liest die Rohdaten aus dem angeschlossenen Temperatursensor.
    #
    # @param self Object pointer
    # @return lines Enthält die Rohdaten der ausgelesenen Werte des Temperatursensors.
    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    ## Diese Funktion liest den aktuellen Wert der Temperatur als lesbaren Zahlenwert.
    #
    # @param self Object pointer
    # @return temp_c Enthält die Temperatur als Wert in Celsius.
    # @return temp_f Enthält die Temperatur als Wert in Fahrenheit.
    def read_temp(self):
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self.read_temp_raw()

        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f

    ## Diese Funktion zeigt die Zeit digital an.
    #
    # @param self Object pointer
    # @param matrix Es wird die Matrix übergeben, die die Zeit digital anzeigen soll.
    def display_digital_time_mode(self, matrix):
        datetime = time.localtime()
        hours = datetime[3]
        minutes = datetime[4]

        minutes_ones = int(minutes % 10)
        hours_ones = int(hours % 10)
        minutes_tens = int((minutes - minutes_ones)*0.1)
        hours_tens = int((hours - hours_ones)*0.1)

        h_o = Number(6, 0, hours_ones)
        h_t = Number(0, 0, hours_tens)
        m_o = Number(6, 8, minutes_ones)
        m_t = Number(0, 8, minutes_tens)

        colon = [16, 17, 31, 32, 61, 62, 76, 77]

        if matrix.get_colon_visibility():
            for i in colon:
                offset = 11
                self.matrix.pixels[i + offset].set_state(True)
            matrix.set_colon_visibility(False)
        elif not matrix.get_colon_visibility():
            matrix.set_colon_visibility(True)

        for i in h_o.visible_pixels:
            offset = h_o.y * 15 + h_o.x
            matrix.pixels[i + offset].set_state(True)

        for i in h_t.visible_pixels:
            offset = h_t.y * 15 + h_t.x
            matrix.pixels[i + offset].set_state(True)

        for i in m_o.visible_pixels:
            offset = m_o.y * 15 + m_o.x
            matrix.pixels[i + offset].set_state(True)

        for i in m_t.visible_pixels:
            offset = m_t.y * 15 + m_t.x
            matrix.pixels[i + offset].set_state(True)

        # print(matrix.getColonVisibility())
        matrix.draw_pixels()

    ## Diese Funktion erlaubt das setzen eines RGB-Farbwerts für alle eingeschalteten Pixel der Uhr.
    #
    # @param rgb_color Ist ein RGB-Wert als Liste der Form [R, G, B]. RGB hat jeweils integer Werte von 0-255.
    # 24-bit Farben. 8-bit je Farbe.
    def set_wordclock_colour_on(self, rgb_colour):
        self.matrix.set_pixel_on_colour(rgb_colour)

    ## Diese Funktion erlaubt das setzen eines RGB-Farbwerts für alle ausgeschalteten Pixel der Uhr.
    #
    # @param rgb_color Ist ein RGB-Wert als Liste der Form [R, G, B]. RGB hat jeweils integer Werte von 0-255.
    # 24-bit Farben. 8-bit je Farbe.
    def set_wordclock_colour_off(self, rgb_colour):
        self.matrix.set_pixel_off_colour(rgb_colour)

    ## Diese Funktion aktualisiert die angezeigten Pixel der WordClock.
    #
    # @param self Object pointer
    def refresh_wordclock(self):
        self.matrix.draw_pixels()

    ## Diese Funktion legt eine übergebene Liste von Pixeln auf die Wortuhr.
    #
    # @param self Object pointer
    # @param pixel_list Dictionary mit 225 RGB Werten. Aufsteigend von links oben nach rechts unten. Dictionary muss
    # folgendermaßen kodiert sein: {"r": 0-255, "g": 0-255, "b": 0-255}.
    def display_custom_pixel_list(self, matrix, pixel_list):
        i = 0
        dim_led = 0.1
        while i < len(pixel_list):
            matrix.set_pixel_colour_rgb(i, pixel_list[i]["r"] * dim_led, pixel_list[i]["g"] * dim_led,
                                        pixel_list[i]["b"] * dim_led)
            i += 1
        matrix.draw_every_single_pixel()
