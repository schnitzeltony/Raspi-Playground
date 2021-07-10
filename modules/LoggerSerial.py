import serial
import threading
import re
from datetime import datetime
from .KeyboardStopper import AbortSingleton

class LoggerSerialBase:
    keyboardStopper = AbortSingleton()
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
        print("Log file " + logFileName + " opened")
        self.logFile.write("Logging started at: " + str(datetime.now()) + '\n\n\n')
        self.thread = threading.Thread(target = self.__threadFunc)
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
    def __init__(self, searchString, logString, ignoreOnEmptySet = []):
        self.searchString = searchString
        self.logString = logString
        self.ignoreOnEmptySet = ignoreOnEmptySet

class LoggerFilterNotify(LoggerSerialBase):
    def __init__(self, label, deviceName, baudRate, logFileName, searchEntries = []):
        super().__init__(label, deviceName, baudRate, logFileName)
        self.lock = threading.Lock()
        self.searchEntries = searchEntries
        self.messages = []

    def getMessages(self):  # other thread
        self.lock.acquire()
        messages = self.messages
        self.messages = []
        self.lock.release()
        return messages
    
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
                    if entry.ignoreOnEmptySet != []:
                        for ignoreStr in entry.ignoreOnEmptySet:
                            if ignoreStr in line:
                                toIgnore = True
                                break
                    if not toIgnore:
                        message = line
                if message != '':
                    self.lock.acquire()
                    self.messages.append(str(datetime.now())  + ' / ' + self.label + ': ' + message)
                    self.lock.release()
                    break
