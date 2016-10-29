# -*- coding: utf-8 -*-
import glob
import RPi.GPIO as GPIO
import time


def read_temp():
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f


def read_adc(adcChannel):
    GPIO.setwarnings(False)
    try:
        GPIO.setmode(GPIO.BCM)
    except ValueError:
        pass
    HIGH = True
    LOW = False
    SCLK = 11
    MOSI = 10
    MISO = 9
    CS = 8
    ADC_TYPE = {'MCP3204': 12, 'MCP3008': 10}
    GPIO.setup(SCLK, GPIO.OUT)
    GPIO.setup(MOSI, GPIO.OUT)
    GPIO.setup(MISO, GPIO.IN)
    GPIO.setup(CS, GPIO.OUT)
    GPIO.output(SCLK, LOW)
    GPIO.output(CS, HIGH)
    GPIO.output(CS, LOW)
    sendcmd = adcChannel
    sendcmd |= 0b00011000
    # Senden der Bitkombination
    for i in range(5):
        if(sendcmd & 0x10):
            GPIO.output(MOSI, HIGH)
        else:
            GPIO.output(MOSI, LOW)
        # Negative Flanken des Clocksignals generieren
        GPIO.output(SCLK, HIGH)
        GPIO.output(SCLK, LOW)
        sendcmd <<= 1 # Bitfolge eine Position nach links schieben

    # Empfangen der Daten vom MCP3204
    adcvalue = 0 # gelesenen Wert zurueccksetzen
    for i in range(ADC_TYPE['MCP3008'] + 1):
        GPIO.output(SCLK, HIGH)
        GPIO.output(SCLK, LOW)
        adcvalue <<= 1 # 1 Position nach links schieben
        if GPIO.input(MISO):
            adcvalue |= 0x01

    # mit Multimeter ausgemessene Referenzspannung am ADC anliegend, idealerweise eine Referenzspannungsquelle [V]
    u_ref = 3.28
    # 12 Bit = 4096 steps
    bits = 2**ADC_TYPE['MCP3008']
    u_step = u_ref / bits
    u_measured = adcvalue * u_step
    return u_measured
