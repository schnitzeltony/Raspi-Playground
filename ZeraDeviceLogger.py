#!/usr/bin/env python3

import time
from modules.KeyboardStopper import AbortSingleton
from modules.LoggerFactory import LoggerFactory

keyboardStopper = AbortSingleton()
loggerFactory = LoggerFactory('configurations/SerialLogger.json')

print()

while not keyboardStopper.abortRequested():
    time.sleep(0.1)
    loggerFactory.printLogs()

print('Done')