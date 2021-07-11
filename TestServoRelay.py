#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import logging
from modules.LoggingSetup import LoggingSetup
from modules.Duts import DUTs

# init
LoggingSetup('TestServos.log')
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
                logging.info('Release button on %s' % dut['Label'])
                dut['Servo'].moveToPosition(dut['ServoReleasePos'], True)
            if 'Relay' in dut:
                logging.info('Relay on at %s' % dut['Label'])
                dut['Relay'].switch(False)
        logging.info('Sleep %.1fs...' % pause)
        time.sleep(pause)

        # on/pressed
        for dut in duts:
            if 'Servo' in dut:
                logging.info('Press button on %s' % dut['Label'])
                dut['Servo'].moveToPosition(dut['ServoPushPos'], False)
            if 'Relay' in dut:
                logging.info('Relay off at %s' % dut['Label'])
                dut['Relay'].switch(True)
        logging.info('Sleep %f.1s...' % pause)
        time.sleep(pause)

except KeyboardInterrupt:
    pass

GPIO.cleanup()
