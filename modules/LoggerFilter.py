import logging

class LoggerFilterEntry:
    def __init__(self, searchString, logString, ignoreStrSet = [], logLevel = logging.INFO):
        self.searchString = searchString
        self.logString = logString
        self.ignoreStrSet = ignoreStrSet
        self.logLevel = logLevel

class LoggerFilter:
    def __init__(self, logger, filters, label):
        logger.addLogConsumer(self)
        self.filters = filters
        self.label = label
        self.hasCriticalFilters = False
        for filter in filters:
            if filter.logLevel == logging.CRITICAL:
                self.hasCriticalFilters = True
                break
        self.criticalMessageCount = 0

    def parseLine(self, line): # log thread
        message = ''
        for entry in self.filters:
            lineUpper = line.upper()
            searchUpper = entry.searchString.upper()
            if searchUpper in lineUpper:
                if entry.logString != '':
                    message = entry.logString
                else:
                    toIgnore = False
                    if entry.ignoreStrSet != []:
                        for ignoreStr in entry.ignoreStrSet:
                            if ignoreStr in line:
                                toIgnore = True
                                break
                    if not toIgnore:
                        message = line
                if message != '':
                    logging.log(entry.logLevel, self.label + ': ' + message)
                    if entry.logLevel == logging.CRITICAL:
                        self.criticalMessageCount = self.criticalMessageCount + 1
                    break
