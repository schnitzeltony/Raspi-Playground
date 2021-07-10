from .SerialLogger import *

class MT310s2SystemControllerLogger(SerialLoggerFilterNotify):
    def __init__(self, label, deviceName, logFileName):
        searchEntries = [
            SerialLoggerFilterEntry('Power-Button pushed by user', 'Power-button pressed'),
            SerialLoggerFilterEntry('Systemaktivitätszustandsänderung: System ist aktiv', 'System activated'),
            SerialLoggerFilterEntry('-- System-Power-Controller', 'Power on'),
            SerialLoggerFilterEntry('LCD-Backlight', ''),
            SerialLoggerFilterEntry('EEPROM-Save', ''),
            SerialLoggerFilterEntry('USV aktiv halten: Deaktiviert', 'Power off\n'),
            SerialLoggerFilterEntry('Error', '', ['#Monitor:FPGAError'])
                         ]
        super().__init__(label, deviceName, 9600, logFileName, searchEntries)
