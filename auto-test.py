#!/usr/bin/env python3

import RPi.GPIO as GPIO
import threading
import time

class Servo():
  def moveToPosition(self, position, idleAfterReach = True, moveDuration = 0.0):
      self.pwm.ChangeDutyCycle(self.__calcDutyCycle(position))
      positionDiff = abs(self.lastPosition - position) if self.lastPosition >= 0 else 1.0
      expectedDuration = positionDiff * self.fullMoveTimeSeconds
      if moveDuration > expectedDuration:
          self.__timerCleanup()
          self.timer = threading.Timer(self.slowMoveChangeTimeSeconds, self.__slowMoveTimerCallback)
          self.timer.start()
      elif idleAfterReach:
          self.__timerCleanup()
          self.timer = threading.Timer(expectedDuration, self.__idleTimerCallback)
          self.timer.start()
      self.lastPosition = position

  def __init__(self, gpioPin, fullMoveTimeSeconds = 1.0, slowMoveChangeTimeSeconds = 1/10):
      self.GPIO = GPIO.setup(gpioPin, GPIO.OUT)
      self.pwm = GPIO.PWM(gpioPin, 50)
      self.pwm.start(0.0)
      self.fullMoveTimeSeconds = fullMoveTimeSeconds
      self.slowMoveChangeTimeSeconds = slowMoveChangeTimeSeconds
      self.lastPosition = -1.0
      self.timer = None

  def __del__(self):
      self.pwm.stop()
      self.__timerCleanup()

  def __calcDutyCycle(self, position): # position 0-1
      dutyCycleMs = 1+position # 1-2ms
      return dutyCycleMs * 100.0 / 20.0 # pecent / 20ms cycle

  def __idleTimerCallback(self):
      self.__timerCleanup()
      self.pwm.ChangeDutyCycle(0.0)

  def __slowMoveTimerCallback(self):
      self.__timerCleanup()
      self.pwm.ChangeDutyCycle(0.0)

  def __timerCleanup(self):
      if(self.timer):
          self.timer.cancel()
          del self.timer
          self.timer = None

class OnOffServo(Servo):
  def switch(self, on):
      self.moveToPosition(self.onPos if on else self.offPos, not on)

  def __init__(self, gpioPin, offPos = 0.25, onPos = 0.70, fullMoveTimeSeconds = 1.0, slowMoveChangeTimeSeconds = 1/10):
      Servo.__init__(self, gpioPin, fullMoveTimeSeconds, slowMoveChangeTimeSeconds)
      self.offPos = offPos 
      self.onPos = onPos 


class Relay():
  def __init__(self, gpioPin):
      self.GPIO = GPIO.setup(gpioPin, GPIO.OUT)


# init
GPIO.setmode(GPIO.BCM)
pause = 2.0
servos = { OnOffServo(17), OnOffServo(27) }

# loop
try:
    while True:
        for servo in servos:
            servo.switch(False)
        time.sleep(pause)

        for servo in servos:
            servo.switch(True)
        time.sleep(pause)
except KeyboardInterrupt:
    del servos
    GPIO.cleanup()
