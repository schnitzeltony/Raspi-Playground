#!/usr/bin/env python3

import time
from KeyboardStopper import AbortSingleton
from SerialLogger import SerialLoggerSystem

keyboardStopper = AbortSingleton()
sysLogger = SerialLoggerSystem("SystemController", "/dev/ttyUSB0", 9600, "SystemController.log")

print()

while not keyboardStopper.abortRequested():
    time.sleep(0.1)
    messages = sysLogger.getMessages()
    for message in messages:
        print(message)

print('Done')