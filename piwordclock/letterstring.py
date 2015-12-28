# -*- coding: utf-8 -*-
__author__ = 'Valentin'
import time
from .pixel import Pixel
import definitions as d

## Die Klasse Letterstring beschreibt eine Reihe von Buchstaben, die auf der Matrix angezeigt werden können.
#
# Sie berechnet auf die Bewegung über die Matrix der WordClock.
class Letterstring(object):
    """A class which describes a set of letters, its visible pixels and its position in the Matrix of the WordClock.

    It also calculates the new position of the letters while running the letter over the WordClock."""
    def __init__(self, string, x, y):
        self.string = string
        self.length_of_string = len(string)
        self.offset_x = x
        self.offset_y = y
        self.visible_pixels = []
        self.letters = []
        self.letter_matrix = []
        self.index = 0
        self.letter_matrix_pixel = self.length_of_string * 40 + self.length_of_string * 8
        self.letter_matrix_cols = self.length_of_string * 6
        self.move_offset_x = x
        # Creates a matrix with the necessary amount of pixels
        while self.index < self.letter_matrix_pixel:
            self.letter_matrix.append(Pixel(False, "green", self.index % self.letter_matrix_cols,
                                            int(self.index/self.letter_matrix_cols)))
            self.index += 1
        for i in self.string:
            j = d.letters.find(i)
            self.visible_pixels.append(d.listOfLetters[j])
        self.letter_position = 0
        for i in self.visible_pixels:
            for j in i:
                # position = self.letterPosition*6 + j + int(j/6)*(self.lengthOfString-1)*6
                # Calculate coordinates for the visiblePixels
                pos_x = j % 5 + 6 * self.letter_position
                pos_y = int(j / 5)
                # Calculate coordinates back to the appropriate pixel number in letterMatrix
                position = self.letter_matrix_cols * pos_y + pos_x
                self.letter_matrix[position].set_state(True)
            self.letter_position += 1

    def overlay_matrix(self, matrix):
        # Checks if all letters run through the matrix
        while self.move_offset_x > -self.letter_matrix_cols:
            matrix.clear_all_pixels()
            for i in self.letter_matrix:
                if i.get_state() and i.x+self.move_offset_x < 15 and i.y+self.offset_y < 15\
                        and i.x+self.move_offset_x >= 0 and i.y+self.offset_y >= 0:
                    new_x = i.x+self.move_offset_x
                    new_y = i.y+self.offset_y
                    new_position_in_matrix = new_y*15 + new_x
                    matrix.set_pixel_state(new_position_in_matrix, True)
                    #matrix.draw_pixels()
                    #time.sleep(0.05)
                else:
                    continue
            self.move_offset_x -= 1
            matrix.draw_pixels()
            # if self.move_offset_x == - self.letter_matrix_cols:
                # break
                # self.move_offset_x = self.offset_x
                # time.sleep(1)
            time.sleep(0.04)