import json
import logging
from .LoggerLinuxConsoleImx6 import LoggerLinuxConsoleImx6
from .LoggerMT310s2SystemController import LoggerMT310s2SystemController

class LoggerFactory:
    def __init__(self, configurationFileName):
        file = open(configurationFileName, 'r')
        configuration = json.load(file)
        file.close()

        self.duts = []
        self.loggers = []
        dutsLabels = []
        ttys = []
        for dut in configuration['duts']:
            try:
                dutLabel = dut['label']
                if dutLabel in dutsLabels:
                    raise RuntimeWarning("Double dut in: %s" % dut)
                dutsLabels.append(dutLabel)
                for port in dut['ports']:
                    tty = port['tty']
                    if tty in ttys:
                        raise RuntimeWarning("tty already in use: %s" % dut)
                    ttys.append(tty)
                    type = port['type']
                    label = dutLabel + '-' + type
                    if type == 'Linux-Console':
                        dut['linuxLogger'] = LoggerLinuxConsoleImx6(label, tty, label + '.log')
                        self.loggers.append(dut['linuxLogger'])
                    elif type == 'Systemcontroller':
                        dut['systemControllerLogger'] = LoggerMT310s2SystemController(label, tty, label + '.log')
                        self.loggers.append(dut['systemControllerLogger'])
                    else:
                        raise RuntimeWarning("Unknown logger type for: %s" % dut)
                self.duts.append(dut)

            except RuntimeWarning as e:
                logging.warn("Could not load dut: %s" % dut)
                logging.warn(e)
            except (OSError, IOError) as e:
                logging.warn('An error occured opening logger dut:')
                logging.warn(e)

    def allFailedCritical(self):
        failedAll = True
        for logger in self.loggers:
            if logger.loggerFilter.hasCriticalFilters:
                if logger.loggerFilter.criticalMessageCount == 0:
                    failedAll = False
                    break
        return failedAll

    def showCriticalResults(self):
        for logger in self.loggers:
            if logger.loggerFilter.hasCriticalFilters:
                if logger.loggerFilter.criticalMessageCount > 0:
                    logging.critical(logger.logger.label + ' has critical errors')
                else:
                    logging.info('\x1b[92m' + logger.logger.label + ' has no critical errors' + '\x1b[0m' )

    def writeResultsToDevice(self, powerUpCount):
        for dut in self.duts:
            if 'linuxLogger' in dut:
                logger = dut['linuxLogger']
                logging.info(logger.logger.label + ': write test-results to device')
                logger.loginConsole()
                result = {'powerUpCount': powerUpCount, 'failCount': logger.loggerFilter.criticalMessageCount }
                jsonstr = json.dumps(result, indent = 4)
                shellCmd = 'echo \'%s\' > ~/endurance-result.json' % jsonstr
                logger.execShell(shellCmd)
