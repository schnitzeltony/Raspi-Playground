from .LoggerSerial import *
from .LoggerFilter import *

class LoggerLinuxConsoleImx6():
    def __init__(self, label, deviceName, logFileName):
        self.logger = LoggerSerialBase(label, deviceName, 115200, logFileName)
        filterEntries = [
            LoggerFilterEntry('u-boot', ''),
            LoggerFilterEntry(' login: ', 'Console login reached'),
            LoggerFilterEntry('Started Zera Module Manager.', 'Modulemanager started'),
            LoggerFilterEntry('Started Zera DSP daemon.', 'DSP service started'),
            LoggerFilterEntry('Started SEC1000 daemon', 'Error calculator service started'),
            LoggerFilterEntry('Started Zera Resource Manager.', 'Resource manager service started'),
            LoggerFilterEntry('mounting fs with errors', 'File system reported trouble', [], logging.WARNING),
            LoggerFilterEntry('usb 2-1: device descriptor', 'USB: down/in trouble?', [], logging.WARNING),
            LoggerFilterEntry('usb 2-1: device not accepting', 'USB: down/in trouble?', [], logging.WARNING),
            LoggerFilterEntry('Error', '',
                                    ['cannot determine file size', 'ti-connectivity', 'regulatory.db', 'firmware load for vpu_fw_imx6q.bin'],
                                    logging.ERROR)
                         ]
        self.loggerFilter = LoggerFilter(self.logger, filterEntries, label)
