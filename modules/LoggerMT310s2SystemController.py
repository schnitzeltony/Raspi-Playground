import logging
from .LoggerSerial import *

class LoggerMT310s2SystemController(LoggerFilterNotify):
    def __init__(self, label, deviceName, logFileName):
        searchEntries = [
            LoggerFilterEntry('Power-Button pushed by user', 'Power-button pressed'),
            LoggerFilterEntry('Systemaktivitätszustandsänderung: System ist aktiv', 'System activated'),
            LoggerFilterEntry('-- System-Power-Controller', 'Power on'),
            LoggerFilterEntry('LCD-Backlight', ''),
            LoggerFilterEntry('EEPROM-Save', ''),
            LoggerFilterEntry('USV aktiv halten: Deaktiviert', 'Power off\n'),
            LoggerFilterEntry('Error', '', ['#Monitor:FPGAError'], logging.WARNING)
                         ]
        super().__init__(label, deviceName, 9600, logFileName, searchEntries)
