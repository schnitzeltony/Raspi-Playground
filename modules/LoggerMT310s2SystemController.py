from .LoggerSerial import *
from .LoggerFilter import *

class LoggerMT310s2SystemController():
    def __init__(self, label, deviceName, logFileName):
        self.logger = LoggerSerialBase(label, deviceName, 9600, logFileName)
        filterEntries = [
            LoggerFilterEntry('Power-Button pushed by user', 'Power-button pressed'),
            LoggerFilterEntry('Systemaktivitätszustandsänderung: System ist aktiv', 'System activated'),
            LoggerFilterEntry('-- System-Power-Controller', 'Power on'),
            LoggerFilterEntry('LCD-Backlight', ''),
            LoggerFilterEntry('EEPROM-Save', ''),
            LoggerFilterEntry('USV aktiv halten: Deaktiviert', 'Power off\n'),
            LoggerFilterEntry('Warning', '', [], logging.WARNING),
            LoggerFilterEntry('Error', '', ['#Monitor:FPGAError'], logging.WARNING)
                         ]
        self.loggerFilter = LoggerFilter(self.logger, filterEntries, label)
