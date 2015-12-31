# -*- coding: utf-8 -*-
__author__ = 'Valentin'

import time
import math

#TODO Funktion zum Faden aller LEDs die ihre Farbe ändern sollen.
#TODO Funktion muss am Besten an passender Stelle aufrufbar sein. Vorschlag: in matrix.draw_pixels()

## Einfache Testfunktion um das Fading einer LED zu berechnen.
#
# Es wird ein neuer und ein aktueller Farbwert der LED vorgegeben. Die LED soll über einen gegebenen Zeitraum die Farbe
# gleichmäßig ändern.
# @param rgb_new Neuer Farbwert als Liste mit 3 Werten in der Reihenfolge rot, grün, blau.
# @param rgb_current Aktueller Farbwert als Liste mit 3 Werten in der Reihenfolge rot, grün, blau.
# @param time Zeitintervall in der die Änderung abgeschlossen sein soll in Sekunden.
def fade_led(rgb_new, rgb_current, time):
    r_step = rgb_new[0] - rgb_current[0]
    g_step = rgb_new[1] - rgb_current[1]
    b_step = rgb_new[2] - rgb_current[2]

    rgb_step = [math.fabs(r_step), math.fabs(g_step), math.fabs(b_step)]
    #TODO min_step darf nicht 0 werden
    min_step = min(rgb_step)

    # time_step in seconds
    time_step = time / min_step

    r_step_size = r_step / min_step
    g_step_size = g_step / min_step
    b_step_size = b_step / min_step

    print(min_step, time_step, r_step_size, b_step_size, g_step_size)

    t = time_step
    r_val = rgb_current[0]
    g_val = rgb_current[1]
    b_val = rgb_current[2]

    while t < time:
        r_val = int(round(r_val + r_step_size, 0))
        g_val = int(round(g_val + g_step_size, 0))
        b_val = int(round(b_val + b_step_size, 0))
        print(t, r_val, g_val, b_val)
        t = t + time_step


new = [0, 0, 0]
current = [10, 10, 10]
fade_led(new, current, 1)

