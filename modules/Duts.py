import json
from .Servo import Servo
from .Relay import Relay

class DUTs:
    def __init__(self, configurationFileName):
        try:
            self.DUTs = []
            file = open(configurationFileName, 'r')
            configuration = json.load(file)
            for entry in configuration['DUTs']:
                try:
                    if not 'Label' in entry:
                        raise Exception("DUT has no label in: %s" % entry)
                    if 'ServoGPIO' in entry:
                        # check for mandatory
                        if 'ServoPushPos' in entry and 'ServoReleasePos' in entry:
                            entry["Servo"] = Servo(entry['ServoGPIO'])
                        else:
                            raise Exception("Servo definition imcomplete - ServoPushPos/ServoReleasePos are mandatory in: %s" % entry)
                    if 'RelayGPIO' in entry:
                        entry["Relay"] = Relay(entry['RelayGPIO'])
                    self.DUTs.append(entry)
                except Exception as e:
                    print("Could not load DUT: %s" % entry)
                    print(e)
            file.close()
        except Exception as e:
            print("An error occured loading DUTS:")
            print(e)

    def getDuts(self):
        return self.DUTs
