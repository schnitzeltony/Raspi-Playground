#!/usr/bin/env python3

import time
import logging
from modules.LoggingSetup import LoggingSetup
from modules.KeyboardStopper import AbortSingleton
from modules.LoggerFactory import LoggerFactory

keyboardStopper = AbortSingleton()

LoggingSetup('ZeraDevices.log')
loggerFactory = LoggerFactory('configurations/SerialLogger.json')

logging.info("Logger init done\n")

while not keyboardStopper.abortRequested():
    time.sleep(0.1)

logging.info("Done")