# -*- coding: utf-8 -*-
__author__ = 'Valentin'

import json

if __name__ == '__main__':
    json_file_path = "../config.json"
    with open(json_file_path) as json_raw_data:
        config_data = json.load(json_raw_data)
        print("WordClock Version: " + config_data["WordClock Version"])
        print("Binary Mode: " + str(config_data["Binary Mode"]))
        start_up_colors_on = config_data["Start Up On Color"]
        print("Start Up Color On Values: " + "R: " + str(start_up_colors_on["red"]) + " G: " +
              str(start_up_colors_on["green"]) + " B: " + str(start_up_colors_on["blue"]))
        start_up_colors_off = config_data["Start Up Off Color"]
        print("Start Up Color Off Values: " + "R: " + str(start_up_colors_off["red"]) + " G: " +
              str(start_up_colors_off["green"]) + " B: " + str(start_up_colors_off["blue"]))
