# -*- coding: utf-8 -*-
__author__ = 'Valentin'
from .pixel import Pixel
import math

## Die Klasse Matrix beschreibt die Matrix von Pixeln die auf der WordClock angezeigt werden.
#
# Beinhaltet eine Reihe von Funktionen die einzelnen Pixel der Matrix zu kontrollieren.
class Matrix(object):
    """Sets up a matrix for the WordClock.

    A Matrix consists of a list of pixels. Each Pixel is a class and has certain atrributes."""
    ## Die Initialisierungsfunktion der Klasse Matrix setzt eine Matrix aus der Anzahl der übergebenen Pixel auf.
    #
    # Die Funktion arbeitet zur Zeit nur korrekt bei quadratischen Matrizen mit 225 Pixeln. Evtentuell sollte die
    # Funktion an dieser Stelle flexibler sein. Bisher aber nicht nötig.
    # @param pixel Anzahl der Pixel in Reihe
    # @param strip Muss ein Objekt aus der Klasse Neopixel sein. Auf diesem werden die Funktionen zur Anzeige der
    # Uhrzeit ausgeführt.
    def __init__(self, pixel, binary_extension, strip):
        i = 0
        self.strip = strip
        self.pixels = []
        self.colonVisible = False
        self.pixel_colour_on = [0, 0, 150]
        self.pixel_colour_off = [0, 0, 0]
        self.__binary_extension = binary_extension
        # For each pixel create one pixel object and append it to the  pixels array
        while i <= (pixel+self.__binary_extension)-1:
            self.pixels.append(Pixel(False, i % 15, int(i/15), "yellow", "white"))
            i += 1

    ## Gibt den Status eines bestimmten Pixels in der Reihe zurück.
    #
    # @return True für an und False für aus.
    def get_pixel_state(self, pixel):
        return self.pixels[pixel].get_state()

    ## Setzt den Status einen Pixels an einer bestimmten Stelle in der Reihe.
    #
    # @param pixel_no Nummer des Pixels.
    # @param state True für an und False für aus.
    def set_pixel_state(self, pixel_no, state):
        self.pixels[pixel_no].set_state(state)

    ## Setzt die Farbe eines Pixels.
    #
    # @param pixel_no Nummer des Pixels.
    # @param state True für an und False für aus.
    # @param r Wert für Rot von 0-255.
    # @param g Wert für Grün von 0-255.
    # @param b Wert für Blau von 0-255.
    def set_pixel_colour_rgb(self, pixel_no, r, g, b):
        self.pixels[pixel_no].state = True
        self.pixels[pixel_no].colour_on = [r, g, b]

    ## Diese Funktion aktualisiert die Anzeige der Uhr. Sie übernimmt dabei alle Informationen der einzelnen Pixel. Der
    # Farbwert der Pixel wird nicht übernommen sondern Allgemein aus den Matrixvariablen pixel_colour_on und
    # pixel_colour_off abgerufen.
    #
    # Anhand der Anzahl der Pixel errechnet die Funktion die korrekte Reihenfolge der Pixel. Diese
    # ist aber abhängig von der internen Verdahtung der Pixel und muss gegebenenfalls korrigiert werden. Die eigentliche
    # Farbe der einzelnen Pixel wird hier noch nicht berücksichtigt sondern nur eine Allgemeine global gesetzte. Dies
    # muss noch implementiert werden.
    # @param self Object pointer
    def draw_pixels(self):
        # Den drei unteren Pixel könnte man auch ihre Nummern entsprechend der Matrix geben
        # (Reihe 15 invertiert 239, 240, 241), dann kann man sich die Unterscheidung sparen
        for i in range(0, len(self.pixels) - self.__binary_extension):
            row = int((i - i % 15)/15)
            if row % 2 == 0:
                i_new = i
            else:
                i_new = row * 30 + 14 - i
            if self.pixels[i].state:
                self.strip.setPixelColorRGB(i_new, int(round(self.pixel_colour_on[0], 0)),
                                            int(round(self.pixel_colour_on[1], 0)),
                                            int(round(self.pixel_colour_on[2], 0)))
            else:
                self.strip.setPixelColorRGB(i_new, int(round(self.pixel_colour_off[0], 0)),
                                            int(round(self.pixel_colour_off[1], 0)),
                                            int(round(self.pixel_colour_off[2], 0)))

        # This shows the binary extension leds
        for i in range(len(self.pixels) - self.__binary_extension, len(self.pixels)):
            if self.pixels[i].state:
                self.strip.setPixelColorRGB(i, int(round(self.pixel_colour_on[0], 0)),
                                            int(round(self.pixel_colour_on[1], 0)),
                                            int(round(self.pixel_colour_on[2], 0)))
            else:
                self.strip.setPixelColorRGB(i, int(round(self.pixel_colour_off[0], 0)),
                                            int(round(self.pixel_colour_off[1], 0)),
                                            int(round(self.pixel_colour_off[2], 0)))

        self.strip.show()

    ## Diese Funktion aktualisiert die Anzeige der Uhr. Es werden dabei die einzelnen Farbwerte der Pixel abgerufen.
    #
    # Anhand der Anzahl der Pixel errechnet die Funktion die korrekte Reihenfolge der Pixel. Diese
    # ist aber abhängig von der internen Verdahtung der Pixel und muss gegebenenfalls korrigiert werden.
    # @param self Object pointer
    #TODO Redundante Funktion zu draw_pixels(), kann vermutlich 1:1 ersetzt werden
    def draw_every_single_pixel(self):
        for i in range(0, len(self.pixels) - self.__binary_extension):
            row = int((i - i % 15)/15)
            if row % 2 == 0:
                i_new = i
            else:
                i_new = row * 30 + 14 - i
            if self.pixels[i].state:
                self.strip.setPixelColorRGB(i_new, int(self.pixels[i].colour_on[0]), int(self.pixels[i].colour_on[1]),
                                            int(self.pixels[i].colour_on[2]))
            else:
                self.strip.setPixelColorRGB(i_new, int(self.pixels[i].colour_off[0]), int(self.pixels[i].colour_off[1]),
                                            int(self.pixels[i].colour_off[2]))

        for i in range(len(self.pixels) - self.__binary_extension, len(self.pixels)):
            if self.pixels[i].state:
                self.strip.setPixelColorRGB(i, int(self.pixel_colour_on[0]), int(self.pixel_colour_on[1]),
                                            int(self.pixel_colour_on[2]))
            else:
                self.strip.setPixelColorRGB(i, int(self.pixel_colour_off[0]), int(self.pixel_colour_off[1]),
                                            int(self.pixel_colour_off[2]))

        self.strip.show()

    ## Diese Funktion versetzt alle Pixel in den ausgeschalteten Zustand, ohne die Anzeige zu aktualisieren.
    def clear_all_pixels(self):
        for i in range(0,len(self.pixels)):
            self.pixels[i].set_state(False)
        #self.draw_pixels()

    ## Diese Funktion wird für den digitalen Zeitmodus benötigt. Setzt den Doppekpunkt aktiv oder inaktiv.
    #
    # Wäre besser in der Funktion für den digitalen Zeitmodus aufgehoben, steht aber hier, da es so schneller zu
    # implementieren war.
    # @param self Object pointer
    # @param colon_visible True oder False für entweder aktiv oder inaktiv.
    def set_colon_visibility(self, colon_visible):
        self.colonVisible = colon_visible

    ## Diese Funktion gibt an, ob der Doppelpunkt aktiv oder inaktiv ist.
    #
    # @return True bedeutet aktiv. False bedeutet inaktiv.
    def get_colon_visibility(self):
        return self.colonVisible

    ## Diese Funktion setzt die Farbe aller angezeigten Pixel die Informationen darstellen.
    #
    # @param color Ist ein RGB-Wert als Liste der Form [R, G, B]. RGB hat jeweils Integer Werte von 0-255.
    # 24-bit Farben. 8-bit je Farbe.
    def set_pixel_on_colour(self, colour):
        self.pixel_colour_on = colour

    ## Diese Funktion setzt die Farbe aller nicht angezeigten Pixel. In der Regel leuchten diese nicht.
    #
    # @param color Ist ein RGB-Wert als Liste der Form [R, G, B]. RGB hat jeweils integer Werte von 0-255.
    # 24-bit Farben. 8-bit je Farbe.
    def set_pixel_off_colour(self, colour):
        self.pixel_colour_off = colour