#!/usr/bin/env python3

import time
import logging
from modules.LoggingSetup import LoggingSetup
from modules.KeyboardStopper import AbortSingleton
from modules.LoggerFactory import LoggerFactory
from modules.AutoRun import AutoRun
from modules.ThreadCollector import ThreadCollectorSingleton

pcDebug = False

keyboardStopper = AbortSingleton()

LoggingSetup('ZeraEnduranceTest.log')
loggerFactory = LoggerFactory('configurations/SerialLogger.json')

def callbackLinuxConsoleActive():
    logging.info("callbackLinuxConsoleActive TODO")
autoRun = AutoRun('configurations/AutoRun.json')
autoRun.addCallback(callbackLinuxConsoleActive, 'LinuxConsoleActive')

duts = None
if not pcDebug:
    import RPi.GPIO as GPIO
    from modules.Duts import DUTs

    GPIO.setmode(GPIO.BCM)
    dutsObj = DUTs('configurations/DUTs.json')
    duts = dutsObj.getDuts()
    logging.debug(duts)

while not keyboardStopper.abortRequested():
    if not autoRun.abortOnAllFailed or not loggerFactory.allFailedCritical():
        autoRun.runStep(duts)
        time.sleep(0.1)
    else:
        keyboardStopper.requestAbort()

print()
loggerFactory.showCriticalResults()
print()

logging.info("Wait for all threads to finish")
threadCollector = ThreadCollectorSingleton()
threadCollector.waitForAllToFinish()

if not pcDebug:
    GPIO.cleanup()

logging.info("Done\n\n")

