#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from modules.Duts import DUTs

# init
GPIO.setmode(GPIO.BCM)
pause = 2.0
dutsObj = DUTs('configurations/DUTs.json')
duts = dutsObj.getDuts()


# loop
try:
    while True:
        # off/released
        for dut in duts:
            if 'Servo' in dut:
                print('Release button on %s' % dut['Label'])
                dut['Servo'].moveToPosition(dut['ServoReleasePos'], True)
            if 'Relay' in dut:
                print('Relay on at %s' % dut['Label'])
                dut['Relay'].switch(False)
        print()
        time.sleep(pause)

        # on/pressed
        for dut in duts:
            if 'Servo' in dut:
                print('Press button on %s' % dut['Label'])
                dut['Servo'].moveToPosition(dut['ServoPushPos'], False)
            if 'Relay' in dut:
                print('Relay off at %s' % dut['Label'])
                dut['Relay'].switch(True)
        print()
        time.sleep(pause)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
