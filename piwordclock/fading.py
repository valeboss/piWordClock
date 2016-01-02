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
def fade_led(rgb_new, rgb_current, waiting_time):
    r_step = rgb_new[0] - rgb_current[0]
    g_step = rgb_new[1] - rgb_current[1]
    b_step = rgb_new[2] - rgb_current[2]

    rgb_step = [math.fabs(r_step), math.fabs(g_step), math.fabs(b_step)]

    while True:
        try:
            rgb_step.remove(0)
        except ValueError:
            try:
                min_step = min(rgb_step)
                break
            except ValueError:
                min_step = 1
                break

    # time_step in seconds
    time_step = waiting_time / min_step

    if time_step < 1/50:
        time_step = 1/50
        min_step = 50

    r_step_size = r_step / min_step
    g_step_size = g_step / min_step
    b_step_size = b_step / min_step

    # Multiplikation mit Tausend, da es bei den floats sonst zu Rundungsfehlern kommt
    multiplied_time_step = time_step * 1000
    multiplied_waiting_time = 1000 * waiting_time

    print(min_step, time_step, r_step_size, b_step_size, g_step_size, multiplied_waiting_time, multiplied_time_step)

    t = multiplied_time_step
    r_val = rgb_current[0]
    g_val = rgb_current[1]
    b_val = rgb_current[2]

    while t <= multiplied_waiting_time:
        r_val = r_val + r_step_size
        g_val = g_val + g_step_size
        b_val = b_val + b_step_size
        # Gerundet wird in matrix.draw_pixels(). Hier nur zum Debuggen.
        r_val_led = int(round(r_val, 0))
        g_val_led = int(round(b_val, 0))
        b_val_led = int(round(g_val, 0))
        print(t/1000, r_val_led, g_val_led, b_val_led)
        t += multiplied_time_step
        time.sleep(time_step)


new = [0, 0, 0]
current = [255, 0, 0]
fade_led(new, current, .01)
