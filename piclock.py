# -*- coding: utf-8 -*-
__author__ = 'Valentin'

from piwordclock import wordclock as wc
from piwordclock import sensors
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

pixel_colour_on = [3, 255, 204]
pixel_colour_off = [0, 0, 0]
pixel_list = []
clock_mode = "words"
luminosity = 1.0
colour_lock = threading.Lock()


class ClockThread(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        global colour_lock
        clock = wc.WordClock(15, 15)
        print("Thread started: " + self.name)
        while True:
            colour_lock.acquire()
            try:
                clock.set_wordclock_colour_on([colour * luminosity for colour in pixel_colour_on])
                clock.set_wordclock_colour_off([colour * luminosity for colour in pixel_colour_off])
                clock.run_clock(clock_mode, pixel_list)
            finally:
                colour_lock.release()
            # sleep könnte evtl. in die Funktionen, dann ist es aber schwieriger den Thread zu kontrollieren
            time.sleep(1)


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

    def run(self):
        print("Thread started: " + self.name + ". Checking light intensity every 0.5 secs.")
        while True:
            global luminosity
            luminosity_level = sensors.read_adc(3) / 3.28
            if luminosity_level < 0.004:  # ca.  1/255
                luminosity = 0.004
            elif luminosity_level > 1.0:
                print("Debug information: luminosity level > 1 luminosity_level: " + str(luminosity_level))
                luminosity = 1.0
            else:
                luminosity = luminosity_level
            time.sleep(0.5)


def main():
    while True:
        print("Mainloop running...")
        time.sleep(60)


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
        global colour_lock
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
                colour_lock.acquire()
                try:
                    global pixel_colour_on
                    pixel_colour_on = ([int(message_array[1] * factor), int(message_array[2] * factor),
                                        int(message_array[3] * factor)])
                finally:
                    colour_lock.release()
            elif instruction == "off_colour_rgb":
                colour_lock.acquire()
                try:
                    global pixel_colour_off
                    pixel_colour_off = ([int(message_array[1] * factor), int(message_array[2] * factor),
                                        int(message_array[3] * factor)])
                finally:
                    colour_lock.release()
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
    tornado_thread = TornadoThread(1, "Tornado Websocket Server")
    database_thread = DatabaseThread(2, "sqlite3 Database")
    luminosity_control_thread = LuminosityControlThread(3, "Luminosity Control")
    clock_thread.start()
    tornado_thread.start()
    database_thread.start()
    luminosity_control_thread.start()
    main()
