# -*- coding: utf-8 -*-

from piwordclock import debug_date as dd

debug_time = dd.DebugTime()

for i in range(60*60*24//1800):
    debug_time.user_defined_tick(1800)
    datetime = debug_time.get_datetime()
    print("It is %02u:%02u:%02u o'clock." % (datetime[3], datetime[4], datetime[5]))
