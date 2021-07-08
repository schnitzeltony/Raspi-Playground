#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from Servo import Servo


class Relay():
  def __init__(self, gpioPin):
      self.GPIO = GPIO.setup(gpioPin, GPIO.OUT)


# init
GPIO.setmode(GPIO.BCM)
pause = 2.0
offPos = 0.25
onPos = 0.75

servos = { Servo(17), Servo(27) }
for servo in servos:
    servo.moveToPosition(offPos, True)

# loop
try:
    while True:
        for servo in servos:
            servo.moveToPosition(onPos, False)
        time.sleep(pause)

        for servo in servos:
            servo.moveToPosition(offPos, True)
        time.sleep(pause)
except KeyboardInterrupt:
    pass

del servos
GPIO.cleanup()
