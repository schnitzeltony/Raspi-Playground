#!/usr/bin/env python3

import time
from modules.KeyboardStopper import AbortSingleton
from modules.LoggerMT310s2SystemController import LoggerMT310s2SystemController
from modules.LoggerLinuxConsoleImx6 import LoggerLinuxConsoleImx6

keyboardStopper = AbortSingleton()
sysLogger = LoggerMT310s2SystemController("SystemController", "/dev/ttyUSB0", "SystemController.log")
linuxLogger = LoggerLinuxConsoleImx6("Linux", "/dev/ttyUSB1", "Linux.log")

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