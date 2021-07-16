import serial
import threading
import logging
import re
from datetime import datetime
from .KeyboardStopper import AbortSingleton
from .ThreadCollector import ThreadCollectorSingleton

class LoggerSerialBase:
    keyboardStopper = AbortSingleton()
    threadColletionSingleton = ThreadCollectorSingleton()
    def __init__(self, label, deviceName, baudRate, logFileName):
        self.label = label
        self.serPort = serial.Serial(
            port = deviceName,
            baudrate = baudRate,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
            timeout=1)
        self.serPort.flushInput()

        self.logFile = open(logFileName, "a", encoding='utf-8')
        logging.info("Log file " + logFileName + " opened")
        self.logFile.write("Logging started at: " + str(datetime.now()) + '\n\n\n')

        self.thread = threading.Thread(target = self.__threadFunc)
        LoggerSerialBase.threadColletionSingleton.addThread(self.thread)
        self.thread.start()

        self.logExtraHandlers = []

    def addLogConsumer(self, logConsumer):
        self.logExtraHandlers.append(logConsumer.parseLine)

    def __threadFunc(self):
        regEscape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        while True:
            if LoggerSerialBase.keyboardStopper.abortRequested():
                self.serPort.close()
                self.logFile.close()
                break
            line = self.serPort.readline().decode('unicode-escape').replace('\0', '').replace('\r', '').replace('\n', '')
            escaped = regEscape.sub('', line)
            if escaped != "":
                for extraHandler in self.logExtraHandlers:
                    extraHandler(escaped)
                escaped = str(datetime.now()) + ': ' + escaped
                self.logFile.write(escaped + '\n')
                self.logFile.flush()
    
