from .LoggerSerial import *

class LoggerLinuxConsoleImx6(LoggerFilterNotify):
    def __init__(self, label, deviceName, logFileName):
        searchEntries = [
            LoggerFilterEntry('u-boot', ''),
            LoggerFilterEntry(' login: ', 'Console login reached'),
            LoggerFilterEntry('Started Zera Module Manager.', 'Modulemanager started'),
            LoggerFilterEntry('Started Zera DSP daemon.', 'DSP service started'),
            LoggerFilterEntry('Started SEC1000 daemon', 'Error calculator service started'),
            LoggerFilterEntry('Started Zera Resource Manager.', 'Resource manager service started'),
            LoggerFilterEntry('Error', '',
                                    ['cannot determine file size', 'ti-connectivity', 'regulatory.db'])
                         ]
        super().__init__(label, deviceName, 115200, logFileName, searchEntries)