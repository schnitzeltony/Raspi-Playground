import logging

def LoggingSetup(logFilename, logLevel = logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(logLevel)

    fileFormater = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    fileHandler = logging.FileHandler(logFilename)
    fileHandler.setFormatter(fileFormater)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(CustomFormatter())
    logger.addHandler(consoleHandler)

class CustomFormatter(logging.Formatter):
    """ Logging Formatter to add colors and count warning / errors
        based upon
        https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
    """

    white = "\x1b[38m"
    grey = "\x1b[37;2m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s [%(levelname)s]  %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: white + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)