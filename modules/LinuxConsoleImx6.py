from .SerialLogger import *

class LinuxConsoleImx6(SerialLoggerFilterNotify):
    def __init__(self, label, deviceName, logFileName):
        searchEntries = [
            SerialLoggerFilterEntry('u-boot', ''),
            SerialLoggerFilterEntry(' login: ', 'Console login reached'),
            SerialLoggerFilterEntry('Started Zera Module Manager.', 'Modulemanager started'),
            SerialLoggerFilterEntry('Started Zera DSP daemon.', 'DSP service started'),
            SerialLoggerFilterEntry('Started SEC1000 daemon', 'Error calculator service started'),
            SerialLoggerFilterEntry('Started Zera Resource Manager.', 'Resource manager service started'),
            SerialLoggerFilterEntry('Error', '',
                                    ['cannot determine file size', 'ti-connectivity', 'regulatory.db'])
                         ]
        super().__init__(label, deviceName, 115200, logFileName, searchEntries)
