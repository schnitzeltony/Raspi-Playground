import logging

class LoggerFilterEntry:
    def __init__(self, searchString, logString, ignoreStrSet = [], logLevel = logging.INFO):
        self.searchString = searchString
        self.logString = logString
        self.ignoreStrSet = ignoreStrSet
        self.logLevel = logLevel

