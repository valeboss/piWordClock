# -*- coding: utf-8 -*-
__author__ = 'Valentin'

from piwordclock import config_parser as jp

if __name__ == '__main__':
    json_file_path = "../config.json"
    config_data = jp.read_config_file(json_file_path)
    print("Test print function: ")
    jp.print_configuration(config_data)

    word_clock_version = str(jp.get_wordclock_version(config_data))
    binary_extension_leds = str(jp.get_wordclock_binary_extension_leds(config_data))
    round_mode = str(jp.get_wordclock_round_mode(config_data))
    start_up_on_colors = jp.get_wordclock_start_up_on_color(config_data)
    r_on = str(start_up_on_colors["red"])
    g_on = str(start_up_on_colors["green"])
    b_on = str(start_up_on_colors["blue"])
    start_up_off_colors = jp.get_wordclock_start_up_off_color(config_data)
    r_off = str(start_up_on_colors["red"])
    g_off = str(start_up_on_colors["green"])
    b_off = str(start_up_on_colors["blue"])

    print("\nTest seperate functions: ")
    print("WordClock Version: " + word_clock_version)
    print("Binary Extension LEDs installed: " + binary_extension_leds)
    print("Round Mode: " + round_mode)
    print("RGB ON: " + r_on + ", " + g_on + ", " + b_on)
    print("RGB OFF: " + r_off + ", " + g_off + ", " + b_off)

