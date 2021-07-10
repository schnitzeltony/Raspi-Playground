import threading
import RPi.GPIO as GPIO

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
        return dutyCycleMs * 100.0 / 20.0 # percent / 20ms cycle

    def __timerCallback(self):
        self.__timerCleanup()
        self.currentPosition = self.targetPosition
        self.pwm.ChangeDutyCycle(0)

    def __timerCleanup(self):
        if(self.timer):
            self.timer.cancel()
            del self.timer
            self.timer = None
