# -*- coding: utf-8 -*-

class DebugTime(object):
    """DebugTime class provides a class for fast testing all times of a day."""

    def __init__(self):
        """Initialises the DateDebug object to 00:00:00."""
        self.__hours = 0
        self.__minutes = 0
        self.__seconds = 0
        self.__minute_tick = 1
        self.__second_tick = 1
        self.__hour_tick = 1

    def user_defined_tick(self, second_tick):
        """Ticks the time further about the given seconds."""
        if self.__seconds < 60:
            self.__seconds += second_tick
        if self.__seconds >= 60:
            minute_ticks = self.__seconds // 60
            self.__minutes += minute_ticks
            self.__seconds %= 60
        if self.__minutes >= 60:
            hour_ticks = self.__minutes // 60
            self.__hours += hour_ticks
            self.__minutes %= 60
        if self.__hours >= 24:
            print("24h passed.")
            self.__hours = 0

    def get_hours(self):
        """Returns the hour part of the time."""
        return self.__hours

    def get_minutes(self):
        """Returns the minute part of the time."""
        return self.__minutes

    def get_seconds(self):
        """Returns the second part of the time."""
        return self.__seconds

    def get_datetime(self):
        """Returns an array similar to datetime."""
        return [[], [], [], self.__hours, self.__minutes, self.__seconds]

    def print_datetime(self):
        """Prints the current datetime."""
        print("It is %02u:%02u:%02u o'clock." % (self.__hours, self.__minutes, self.__seconds))
