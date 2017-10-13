# -*- coding: utf-8 -*-
__author__ = 'Valentin'

from piwordclock import wordclock as wc
from piwordclock import sensors
from piwordclock import config_parser as cp
import threading
import time
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import json
from tornado.options import define, options
import sqlite3
import datetime
import os.path

pixel_list = []
luminosity = 1.0
offset=0.0
# TODO: Put all that stuff into one class/object
if os.path.isfile("config.json"):
    print("Using configuration specified in 'config.json'.")
    config_data = cp.read_config_file("config.json")
else:
    print("Found no config file, using template file. Please specify your own WordClock configuration in 'config.json'."
          " Please use the template specified as in 'config_template.json':")
    if os.path.isfile("config_template.json"):
        config_data = cp.read_config_file("config_template.json")
    else:
        "Found no template configuration. Please add a configuration file or update the repository."
rgb_on = cp.get_wordclock_start_up_on_color(config_data)
# TODO: Check why its GRB. It should be RGB.
pixel_color_on = [rgb_on['green'], rgb_on['red'], rgb_on['blue']]
rgb_off = cp.get_wordclock_start_up_off_color(config_data)
pixel_color_off = [rgb_off['green'], rgb_off['red'], rgb_off['blue']]
clock_mode = cp.get_wordclock_start_up_mode(config_data) 
binary_extension_leds = cp.get_wordclock_binary_extension_leds(config_data)
round_mode = cp.get_wordclock_round_mode(config_data)
wordclock_version = cp.get_wordclock_version(config_data)
refresh_rate = cp.get_wordclock_refresh_rate(config_data)
fading_mode = cp.get_wordclock_fading_mode(config_data)
cp.print_configuration(config_data)

color_lock = threading.Lock()

# TODO: Put all Thread classes in single files
class ClockThread(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        global color_lock
        clock = wc.WordClock(15, 15, binary_extension_leds, round_mode)
        print("Thread started: " + self.name)
        while True:
            color_lock.acquire()
            try:
                clock.set_wordclock_colour_on([color * luminosity for color in pixel_color_on])
                clock.set_wordclock_colour_off([color * luminosity for color in pixel_color_off])
                clock.run_clock(clock_mode, pixel_list)
            finally:
                color_lock.release()
            # sleep könnte evtl. in die Funktionen, dann ist es aber schwieriger den Thread zu kontrollieren
            time.sleep(refresh_rate)


class TornadoThread(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        tornado.options.parse_command_line()
        app = Application()
        app.listen(options.port)
        print("Thread started: " + self.name + ". Now entering IOloop. Waiting for instructions.")
        tornado.ioloop.IOLoop.instance().start()


class DatabaseThread(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.sqlite_file = '/home/pi/sqlitedb/wordclockdb.sqlite'

    def run(self):
        connection = sqlite3.connect(self.sqlite_file)
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS data (timestamp TEXT PRIMARY KEY, temp REAL, power_measured REAL);')
        connection.commit()
        print("Thread started: " + self.name + ". Database open. Now polling every 30 secs.")
        while True:
            temp = sensors.read_temp()[0]
            #print(temp)
            timestamp = json.dumps(datetime.datetime.today().isoformat())
            #print(timestamp)
            val_ch1_adc = sensors.read_adc(1)
            val_ch2_adc = sensors.read_adc(2)
            val_ch3_adc = sensors.read_adc(3) / 3.28
            i_measured = (val_ch1_adc - val_ch2_adc) * (59.4 / 37.4) * 10
            power_measured = val_ch1_adc * i_measured
            #print(val_ch1_adc * (59.4 / 37.4))
            #print(power_measured)
            format_str = 'INSERT INTO data (timestamp, temp, power_measured) VALUES ({timestamp}, {temp}, {power_measured});'
            sql_command = format_str.format(timestamp=timestamp, temp=temp, power_measured=power_measured)
            cursor.execute(sql_command)
            connection.commit()
            time.sleep(30)
            print("Copied values to database" + self.sqlite_file)


class LuminosityControlThread(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        if wordclock_version == "1":
            self.__light_sensor_adc_channel = 2
        elif wordclock_version == "2":
            self.__light_sensor_adc_channel = 3
        else:
            print("Couldn't detect wordclock version. Setting light sensor ADC channel to 3.")
            self.__light_sensor_adc_channel = 3

    def run(self):
        print("Thread started: " + self.name + ". Checking light intensity every 0.5 secs.")
        while True:
            global luminosity
            luminosity_level = sensors.read_adc(self.__light_sensor_adc_channel) / 3.28
            if luminosity_level < 0.004:  # ca.  1/255
                luminosity = 0.004
            elif luminosity_level > 1.0:
                print("Debug information: luminosity level > 1 luminosity_level: " + str(luminosity_level))
                luminosity = 1.0
            else:
                if not fading_mode:
                    luminosity = luminosity_level
                else:
                    datetime = time.localtime()
                    minutes = datetime[4]
                    seconds = datetime[5]
                    if (minutes % 5) == 4:
                        if seconds >= 52:
                            if offset == 0:
                                offset = 0.05
                            else:
                                offset = 0
                            factor = ((60 - seconds + 1) / 10.0) + offset
                            luminosity = luminosity * factor
            time.sleep(0.5)


def main():
    while True:
        try:
            print("Mainloop running...")
            time.sleep(60)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            #clock_thread.stop()
            #tornado_thread.stop()
            #database_thread.
            #luminosity_control_thread.stop()


define("port", default=8889, help="run on the given port", type = int)


class WebsocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print("One new connection is open")

    def on_close(self):
        print("Connection closed")

    def on_message(self, message):
        print("Received message: " + message)
        self.message_handler(message)

    def message_handler(self, message):
        global pixel_list
        global color_lock
        pixel_list = None
        if message == "get_status":
            print("Got asked for status. Sending status...")
            self.write_message("Preparing status...")
            if clock_thread.is_alive():
                self.write_message("status_clock online")
                print("Sent: status_clock online")
            else:
                self.write_message("status_clock offline")
                print("Sent: status_clock offline")
        else:
            message_array = json.loads(message)
            factor = 255 # Werte von Website zwischen 0...1
            instruction = str(message_array[0])
            print("Received instruction: " + instruction + " in following JSON-String: " + str(message_array))
            if instruction == "on_colour_rgb":
                color_lock.acquire()
                try:
                    global pixel_color_on
                    pixel_color_on = ([int(message_array[1] * factor), int(message_array[2] * factor),
                                       int(message_array[3] * factor)])
                finally:
                    color_lock.release()
            elif instruction == "off_colour_rgb":
                color_lock.acquire()
                try:
                    global pixel_color_off
                    pixel_color_off = ([int(message_array[1] * factor), int(message_array[2] * factor),
                                        int(message_array[3] * factor)])
                finally:
                    color_lock.release()
            elif instruction == "set_mode":
                global clock_mode
                clock_mode = message_array[1]
            elif instruction == "set_rendered_picture":
                message_array.pop(0)
                if len(message_array) == 225:
                    pixel_list = message_array
                    clock_mode = "render_pixel_list"
                    #print(pixel_list[0]["r"], len(pixel_list))
                else:
                    print("Length of Array not equal to number of pixels. Go on in running program.")
            else:
                print("I don't know what to do with this instruction. Sorry :-(")
                pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/WebSocket", WebsocketHandler)
        ]

        settings = dict(
            cookie_secret = "__TODO_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__1",
            template_path = os.path.join(os.path.dirname(__file__), "template"),
            static_path = os.path.join(os.path.dirname(__file__), "static")
            # xsrf_cookies = True
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    clock_thread = ClockThread(0, "WordClock")
    #tornado_thread = TornadoThread(1, "Tornado Websocket Server")
    #database_thread = DatabaseThread(2, "sqlite3 Database")
    luminosity_control_thread = LuminosityControlThread(3, "Luminosity Control")
    clock_thread.start()
    #tornado_thread.start()
    #database_thread.start()
    luminosity_control_thread.start()
    main()
