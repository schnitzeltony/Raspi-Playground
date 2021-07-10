from .SerialLogger import *

class LinuxConsoleImx6(SerialLoggerFilterNotify):
    def __init__(self, label, deviceName, baudRate, logFileName):
        searchEntries = [
            SerialLoggerFilterEntry('u-boot', ''),
            SerialLoggerFilterEntry(' login: ', 'Console login reached'),
            SerialLoggerFilterEntry('Error', '',
                                    ['cannot determine file size', 'ti-connectivity', 'regulatory.db'])
                         ]
        super().__init__(label, deviceName, baudRate, logFileName, searchEntries)
