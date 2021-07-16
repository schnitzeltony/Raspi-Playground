import json
import logging
from .LoggerLinuxConsoleImx6 import LoggerLinuxConsoleImx6
from .LoggerMT310s2SystemController import LoggerMT310s2SystemController

class LoggerFactory:
    def __init__(self, configurationFileName):
        try:
            file = open(configurationFileName, 'r')
            configuration = json.load(file)
            file.close()

            self.loggers = []

            for entry in configuration['loggers']:
                try:
                    tty = entry['tty']
                    label = entry['label']
                    if entry['type'] == 'Linux-Console':
                        self.loggers.append(LoggerLinuxConsoleImx6(label, tty, label + '.log'))
                    elif entry['type'] == 'MT310s2-Systemcontroller':
                        self.loggers.append(LoggerMT310s2SystemController(label, tty, label + '.log'))
                    else:
                        raise RuntimeWarning("Unknown logger type for: %s" % entry)
                except RuntimeWarning as e:
                    logging.warn("Could not load logger: %s" % entry)
                    logging.warn(e)
            
        except (OSError, IOError) as e:
            logging.warn('An error occured loading loggers:')
            logging.warn(e)

            