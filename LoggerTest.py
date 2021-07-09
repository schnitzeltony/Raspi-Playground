#!/usr/bin/env python3

import time
from modules.KeyboardStopper import AbortSingleton
from modules.MT310s2SystemController import MT310s2SystemControllerLogger

keyboardStopper = AbortSingleton()
sysLogger = MT310s2SystemControllerLogger("SystemController", "/dev/ttyUSB0", 9600, "SystemController.log")

print()

while not keyboardStopper.abortRequested():
    time.sleep(0.1)
    messages = sysLogger.getMessages()
    for message in messages:
        print(message)

print('Done')