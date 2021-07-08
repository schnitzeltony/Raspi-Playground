#!/usr/bin/env python3

import RPi.GPIO as GPIO
import threading
import time

class Servo():
  # All durations in seconds
  def moveToPosition(self, position, idleAfterReach = False):
      if position < 0.0 or position > 1.0:
          raise ValueError()
      if position == self.currentPosition:
          print("No move required")
          return

      self.__timerCleanup()
      self.targetPosition = position
      if idleAfterReach:
          # else part: at first move we don't know where we are so assume max
          positionDiff = position - self.currentPosition if self.currentPosition >= 0 else 1.0
          expectedDuration = abs(positionDiff) * self.fulldurationDesired
          self.timer = threading.Timer(expectedDuration, self.__timerCallback)
          self.timer.start()
      else:
          self.currentPosition = position
      self.pwm.ChangeDutyCycle(self.__calcDutyCycle(position))

  def __init__(self, gpioPin, fulldurationDesired = 1.0, slowMoveStepDuration = 1/10):
      self.GPIO = GPIO.setup(gpioPin, GPIO.OUT)
      self.pwm = GPIO.PWM(gpioPin, 50)
      self.pwm.start(0.0)
      self.fulldurationDesired = fulldurationDesired
      self.slowMoveStepDuration = slowMoveStepDuration
      self.currentPosition = -1.0
      self.timer = None

  def __del__(self):
      self.pwm.stop()
      self.__timerCleanup()

  def __calcDutyCycle(self, position): # position [0.0;1.0]
      dutyCycleMs = 1+position # 1-2ms
      return dutyCycleMs * 100.0 / 20.0 # pecent / 20ms cycle

  def __timerCallback(self):
      self.__timerCleanup()
      self.currentPosition = self.targetPosition
      self.pwm.ChangeDutyCycle(0)

  def __timerCleanup(self):
      if(self.timer):
          self.timer.cancel()
          del self.timer
          self.timer = None


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
