#!/usr/bin/env python3

import time
from modules.KeyboardStopper import AbortSingleton
from modules.LoggerFactory import LoggerFactory

from modules.LoggerMT310s2SystemController import LoggerMT310s2SystemController
from modules.LoggerLinuxConsoleImx6 import LoggerLinuxConsoleImx6

keyboardStopper = AbortSingleton()
loggerFactory = LoggerFactory('configurations/SerialLogger.json')

print()

while not keyboardStopper.abortRequested():
    time.sleep(0.1)
    loggerFactory.printLogs()

print('Done')