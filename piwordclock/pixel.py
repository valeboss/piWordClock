# -*- coding: utf-8 -*-
__author__ = 'Valentin'

## Die Klasse Pixel beschreibt ein Pixel der WordClock.
class Pixel(object):
    """A pixel describes one pixel in the matrix of the WordClock.

    It holds information about its color, state and position in the WordClock matrix."""
    ## Initialisierungsfunktion erstellt ein Pixel.
    #
    # Benötigt Informationen über Status, Position und Farbe der LED.
    # @param state True für Eingeschaltet, False für ausgeschaltet.
    # @param colour RGB-Farbwert als Liste. [R, G, B] Alternativ python kompatible Farben.
    # @param x Position in x-Richtung. (Horizontal) Beginnend oben links.
    # @param y Position in y-Richtung. (Vertikal) Beginnend oben links.
    def __init__(self, state, x, y, colour_on, colour_off):
        # Status des einzelnen Pixel als Boolean. "True" für aktiv bzw. "False" für inaktiv.
        self.state = state
        # Farbe der eingeschalteten Pixels als RGB-Liste oder Python Farbwert.
        self.colour_on = colour_on
        # Farbe der ausgeschalteten Pixel als RGB-Liste oder Python Farbwert.
        self.colour_off = colour_off
        # Position des Pixels in horizontaler (x-)Richtung.
        self.x = x
        # Position des Pixels in vertikaler (y-)Richtung.
        self.y = y

    ## Diese Funktion ermöglicht es, die Farbe eines einzelnen Pixels zu setzen.
    #
    # Diese Funktion wird zur Zeit nicht genutzt und findet bei der Anzeige durch die Uhr auch keine beachtung.
    # @param self Object pointer
    # @param rgb = RGB-Farbwert als Liste, den das Pixel übernehmen soll.
    def set_colour_on(self, rgb):
        self.colour_on = rgb

    ## Diese Funktion gibt die Farbe des Pixels als RGB Farbwert (Liste) zurück.
    #
    # @param self Object pointer
    # @return color RGB-Farbwert als Liste.
    def get_colour_on(self):
        return self.colour_on

    ## Diese Funktion setzt den Status des Pixels.
    #
    # @param state True für Eingeschaltet, False für ausgeschaltet.
    def set_state(self, state):
        self.state = state

    ## Diese Funktion gibt den Status eines Pixels zurück.
    #
    # @param self Object pointer
    # @return Status des Pixels. True = an; False = aus
    def get_state(self):
        return self.state
