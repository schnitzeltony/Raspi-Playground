#!/usr/bin/env python3

import time
from modules.KeyboardStopper import AbortSingleton
from modules.MT310s2SystemController import MT310s2SystemControllerLogger
from modules.LinuxConsoleImx6 import LinuxConsoleImx6

keyboardStopper = AbortSingleton()
sysLogger = MT310s2SystemControllerLogger("SystemController", "/dev/ttyUSB0", "SystemController.log")
linuxLogger = LinuxConsoleImx6("Linux", "/dev/ttyUSB1", "Linux.log")

print()

while not keyboardStopper.abortRequested():
    time.sleep(0.1)
    messages = sysLogger.getMessages()
    for message in messages:
        print(message)
    messages = linuxLogger.getMessages()
    for message in messages:
        print(message)

print('Done')