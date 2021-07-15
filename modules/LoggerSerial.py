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
                self.parseLine(escaped)
                escaped = str(datetime.now()) + ': ' + escaped
                self.logFile.write(escaped + '\n')
                self.logFile.flush()
    
    def parseLine(self, line):
        pass

class LoggerFilterEntry:
    def __init__(self, searchString, logString, ignoreStrSet = [], logLevel = logging.INFO):
        self.searchString = searchString
        self.logString = logString
        self.ignoreStrSet = ignoreStrSet
        self.logLevel = logLevel

class LoggerFilterNotify(LoggerSerialBase):
    def __init__(self, label, deviceName, baudRate, logFileName, searchEntries = []):
        super().__init__(label, deviceName, baudRate, logFileName)
        self.searchEntries = searchEntries

    def parseLine(self, line): # log thread
        message = ''
        for entry in self.searchEntries:
            lineUpper = line.upper()
            searchUpper = entry.searchString.upper()
            if searchUpper in lineUpper:
                if entry.logString != '':
                    message = entry.logString
                else:
                    toIgnore = False
                    if entry.ignoreStrSet != []:
                        for ignoreStr in entry.ignoreStrSet:
                            if ignoreStr in line:
                                toIgnore = True
                                break
                    if not toIgnore:
                        message = line
                if message != '':
                    logging.log(entry.logLevel, self.label + ': ' + message)
                    break
