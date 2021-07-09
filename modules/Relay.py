import RPi.GPIO as GPIO

class Relay():
    def switch(self, on):
        GPIO.output(self.gpioPin, GPIO.LOW if on else GPIO.HIGH)

    def __init__(self, gpioPin):
        GPIO.setup(gpioPin, GPIO.OUT)
        self.gpioPin = gpioPin
