import json
import logging
from .Servo import Servo
from .Relay import Relay

class DUTs:
    def __init__(self, configurationFileName):
        try:
            file = open(configurationFileName, 'r')
            configuration = json.load(file)
            file.close()

            self.DUTs = []

            for entry in configuration['DUTs']:
                try:
                    if not 'Label' in entry:
                        raise RuntimeWarning("DUT has no label in: %s" % entry)
                    if 'OnOffGPIO' in entry:
                        if not 'OnOffType' in entry:
                            raise RuntimeWarning("DUT definition incomplete - OnOffType is mandatory in: %s" % entry)
                        if entry["OnOffType"] == 'Servo':
                            if 'ServoPushPos' in entry and 'ServoReleasePos' in entry:
                                entry["Servo"] = Servo(entry['OnOffGPIO'])
                            else:
                                raise RuntimeWarning("Servo definition incomplete - ServoPushPos/ServoReleasePos are mandatory in: %s" % entry)
                        elif entry["OnOffType"] == 'Switch':
                            pass
                        else:
                            raise RuntimeWarning("Unknown OnOffType in: %s" % entry)
                    if 'RelayGPIO' in entry:
                        entry["Relay"] = Relay(entry['RelayGPIO'])
                    self.DUTs.append(entry)
                except RuntimeWarning as e:
                    logging.warn("Could not load DUT: %s" % entry)
                    logging.warn(e)
        except (OSError, IOError) as e:
            logging.warn("An error occured loading DUTS:")
            logging.warn(e)

    def getDuts(self):
        return self.DUTs
