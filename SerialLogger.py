import serial
import threading
import re
import string
from datetime import datetime
from KeyboardStopper import AbortSingleton

class SerialLoggerBase:
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
            if SerialLoggerBase.keyboardStopper.abortRequested():
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
    
class SerialLoggerSystem(SerialLoggerBase):
    def getMessages(self):  # other thread
        self.lock.acquire()
        messages = self.messages
        self.messages = []
        self.lock.release()
        return messages
    
    def __init__(self, label, deviceName, baudRate, logFileName):
        super().__init__(label, deviceName, baudRate, logFileName)
        self.lock = threading.Lock()
        self.messages = []
    
    def parseLine(self, line): # log thread
        message = ''
        if 'Nutzer wünscht shutdown' in line:
            message = 'Power-button off detected'
        elif 'Systemaktivitätszustandsänderung: System ist aktiv' in line:
            message = 'System activated'
        elif 'Build-Date:' in line:
            message = "Syscontroller booted"
        elif "LCD-Backlight" in line:
            message = line
        elif 'ERROR' in line:
            message = line
                
        if message != '':
            self.lock.acquire()
            self.messages.append(str(datetime.now())  + ' / ' + self.label + ': ' + message)
            self.lock.release()

    