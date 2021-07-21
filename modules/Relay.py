import RPi.GPIO as GPIO

class Relay():
    def switch(self, on):
        setVal = self.inverted ^ on
        GPIO.output(self.gpioPin, GPIO.HIGH if setVal else GPIO.LOW)

    def __init__(self, gpioPin, inverted = True):
        GPIO.setup(gpioPin, GPIO.OUT)
        self.gpioPin = gpioPin
        self.inverted = inverted
