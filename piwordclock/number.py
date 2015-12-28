# -*- coding: utf-8 -*-
__author__ = 'Valentin'
from piwordclock import definitions as d

## Die Klasse Number beschreibt einfach ein Objekt um eine Zahl auf der Matrix der WordClock darzustellen.
#
# Die Klasse dient einfach nur zur verinfachung der Anzeige von Nummern. Sie beschreibt den Startpunkt der angeziegten Nummer
# obere linke Ecke der Nummer und enthält alle sichtbaren (angeschalteten) Pixel der entsprechenden Nummer.
class Number(object):
    """A class which just describes a number, its visible pixels and its position in the Matrix of the WordClock."""
    ## Initialisierungsfunktion der Klasse Number.
    #
    # @param self Object pointer
    # @param x Position auf der Matrix der WordClock in horizontaler (x-) Richtung.
    # @param y Position auf der Matrix der WordClock in vertikaler (y-) Richtung.
    def __init__(self, x, y, number):
        self.x = x
        self.y = y
        self.number = number
        self.visible_pixels = d.allNumbers[number]