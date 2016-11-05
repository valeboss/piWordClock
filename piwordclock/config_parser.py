# -*- coding: utf-8 -*-
__author__ = 'Valentin'

import json


def read_config_file(path_to_file):
    """Reads the config file in json format and returns it as a dictionary."""
    with open(path_to_file) as json_raw_data:
        config_data = json.load(json_raw_data)

    json_raw_data.close()
    return config_data


def get_wordclock_version(json_data_dict):
    """Returns the WordClock Version."""
    return json_data_dict["WordClock Version"]


def get_wordclock_binary_extension_leds(json_data_dict):
    """Returns if the WordClock has the binary extension set."""
    return json_data_dict["Binary Extension LEDs"]


def get_wordclock_start_up_on_color(json_data_dict):
    """Returns the start up on color of the WordClock as a dictionary."""
    return json_data_dict["Start Up On Color"]


def get_wordclock_start_up_off_color(json_data_dict):
    """Returns the start up off color of the WordClock as a dictionary."""
    return json_data_dict["Start Up Off Color"]


def get_wordclock_round_mode(json_data_dict):
    """Returns if the round mode is enabled or not."""
    return json_data_dict["Round Mode"]

def get_wordclock_start_up_mode(json_data_dict):
    """Returns the Start Up Mode of the WordClock."""
    return json_data_dict["Start Up Mode"]

def get_wordclock_config_data(json_data_dict, data):
    """Returns the given data from a .json data  dictionary."""
    return json_data_dict[data]

def print_configuration(config_data):
    """Prints the current start up configuration of the WordClock."""
    print("--------------------------------------------------")
    print("The current configuration is set as follows:")
    print("WordClock Version: " + str(config_data["WordClock Version"]))
    print("Binary Extension LEDs: " + str(config_data["Binary Extension LEDs"]))
    print("Round Mode: " + str(config_data["Round Mode"]))
    print("WordClock Start Up Mode: "  + str(config_data["Start Up Mode"]))
    start_up_colors_on = config_data["Start Up On Color"]
    print("Start Up Color On Values: " + "R: " + str(start_up_colors_on["red"]) + " G: " +
          str(start_up_colors_on["green"]) + " B: " + str(start_up_colors_on["blue"]))
    start_up_colors_off = config_data["Start Up Off Color"]
    print("Start Up Color Off Values: " + "R: " + str(start_up_colors_off["red"]) + " G: " +
          str(start_up_colors_off["green"]) + " B: " + str(start_up_colors_off["blue"]))
    print("--------------------------------------------------")

