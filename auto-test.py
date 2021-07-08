#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from Servo import Servo
from Relay import Relay

# init
GPIO.setmode(GPIO.BCM)
pause = 2.0
offPos = 0.25
onPos = 0.75

servos = { Servo(17), Servo(27) }
for servo in servos:
    servo.moveToPosition(offPos, True)
relays = { Relay(23), Relay(24) }
for relay in relays:
    relay.switch(False)

# loop
try:
    while True:
        for servo in servos:
            servo.moveToPosition(onPos, False)
        for relay in relays:
            relay.switch(True)
        time.sleep(pause)

        for servo in servos:
            servo.moveToPosition(offPos, True)
        for relay in relays:
            relay.switch(False)
        time.sleep(pause)
except KeyboardInterrupt:
    pass

del servos
GPIO.cleanup()
