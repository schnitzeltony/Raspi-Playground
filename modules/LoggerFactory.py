import json
from os import error
from .LoggerLinuxConsoleImx6 import LoggerLinuxConsoleImx6
from .LoggerMT310s2SystemController import LoggerMT310s2SystemController

class LoggerFactory:
    def __init__(self, configurationFileName):
        try:
            self.loggers = []
            file = open(configurationFileName, 'r')
            configuration = json.load(file)
            for entry in configuration['loggers']:
                try:
                    tty = entry['tty']
                    label = entry['label']
                    if entry['type'] == 'Linux-Console':
                        self.loggers.append(LoggerLinuxConsoleImx6(label, tty, label + '.log'))
                    elif entry['type'] == 'MT310s2-Systemcontroller':
                        self.loggers.append(LoggerMT310s2SystemController(label, tty, label + '.log'))
                    else:
                        raise Exception("Unknown logger type for: %s" % entry)
                except Exception as e:
                    print("Could not load logger: %s" % entry)
                    print(e)
            
            file.close()
        except Exception as e:
            print("An error occured loading loggers:")
            print(e)

    def printLogs(self):
        for logger in self.loggers:
            messages = logger.getMessages()
            for message in messages:
                print(message)
            