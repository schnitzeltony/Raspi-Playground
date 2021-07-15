#!/usr/bin/env python3

import time
import logging
from modules.LoggingSetup import LoggingSetup
from modules.KeyboardStopper import AbortSingleton
from modules.LoggerFactory import LoggerFactory
from modules.ThreadCollector import ThreadCollectorSingleton

keyboardStopper = AbortSingleton()

LoggingSetup('ZeraDevices.log')
loggerFactory = LoggerFactory('configurations/SerialLogger.json')

logging.info("Logger init done\n")

while not keyboardStopper.abortRequested():
    time.sleep(0.1)

logging.info("Wait for logging threads to finish")
threadCollector = ThreadCollectorSingleton()
threadCollector.waitForAllToFinish()

logging.info("Done")