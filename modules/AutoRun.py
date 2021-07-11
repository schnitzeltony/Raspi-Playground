import json
import logging
from datetime import datetime
from datetime import timedelta
from enum import Enum

class AutoStepTypes(Enum):
    INFO = 0
    POWER_ON = 1
    POWER_OFF = 2
    PUSH_BUTTON = 3
    WAIT = 4

class AutoRun:
    def __init__(self, configurationFileName):
        try:
            file = open(configurationFileName, 'r')
            configuration = json.load(file)
            file.close()

            # common settings
            self.buttonPressSeconds = 1.0
            self.onTimeSeconds = 150
            self.powerOffDelaySeconds = 30
            if 'common' in configuration:
                common = configuration['common']
                if 'buttonPressSeconds' in common:
                    self.buttonPressSeconds = common['buttonPressSeconds']
                if 'onTimeSeconds' in common:
                    self.onTimeSeconds = common['onTimeSeconds']
                if 'powerOffDelaySeconds' in common:
                    self.powerOffDelaySeconds = common['powerOffDelaySeconds']

            # restruct loop data for more simple handling
            self.loops = []
            self.loopCounts = []
            for loop in configuration['loops']:
                try:
                    for checkLoop in self.loops:
                        if checkLoop['type'] == loop['type']:
                            raise Exception('Loop of same type already found - ignore loop')
                    if loop['type'] not in ["offTime", "offType", "onDelayType"]:
                        raise Exception('Unknown loop type - ignoring')

                    self.loops.append(loop)
                    self.loopCounts.append(len(loop['values']))
                except Exception as e:
                    logging.warn("Could not load loop: %s" % loop)
                    logging.warn(e)

            self.currentStepNo = -1
            self.currentStepEndTime = datetime.now()
            self.currentSequenceNo = 0
            # build command list
            self.commandList = []
            if len(self.loopCounts) > 0:
                self.loopListCurr = [0] * len(self.loopCounts)
                self.loopEntryCurr = len(self.loopCounts) -1
                while self.__unfold_loop():
                    pass
            else:
                logging.warning('No loops found')

        except Exception as e:
            logging.warn("An error occured loading AutoRun configuration:")
            logging.warn(e)

    def runStep(self, duts):
        if datetime.now() > self.currentStepEndTime:
            # Actions at end of step?
            if self.currentStepNo > 0 and self.commandList[self.currentStepNo]['type'] == AutoStepTypes.PUSH_BUTTON:
                logging.info("*** ReleaseButton ***")
                if duts:
                    for dut in duts:
                        if 'Servo' in dut:
                            logging.info('Action: Release button on %s' % dut['Label'])
                            dut['Servo'].moveToPosition(dut['ServoReleasePos'], True)

            self.currentStepNo = self.currentStepNo + 1
            if self.currentStepNo >= len(self.commandList):
                self.currentStepNo = 0
            if self.currentStepNo == 0:
                self.currentSequenceNo = self.currentSequenceNo + 1
                logging.info("*** Start loop %i ***\n" % self.currentSequenceNo)

            currCmd = self.commandList[self.currentStepNo]
            if 'delay' in currCmd:
                self.currentStepEndTime = datetime.now() + timedelta(seconds = currCmd['delay'])

            if currCmd['type'] == AutoStepTypes.INFO:
                logging.info('*** Start sequence: ' + currCmd['msg'] + ' ***')

            elif currCmd['type'] == AutoStepTypes.POWER_ON:
                logging.info("*** PowerOn ***")
                if duts:
                    for dut in duts:
                        if 'Relay' in dut:
                            logging.info('Action: Relay on at %s' % dut['Label'])
                            dut['Relay'].switch(True)

            elif currCmd['type'] == AutoStepTypes.POWER_OFF:
                logging.info("*** PowerOff ***")
                if duts:
                    for dut in duts:
                        if 'Relay' in dut:
                            logging.info('Action: Relay off at %s' % dut['Label'])
                            dut['Relay'].switch(False)

            elif currCmd['type'] == AutoStepTypes.PUSH_BUTTON:
                logging.info("*** PushButton ***")
                if duts:
                    for dut in duts:
                        if 'Servo' in dut:
                            logging.info('Action: Press button on %s' % dut['Label'])
                            dut['Servo'].moveToPosition(dut['ServoPushPos'], False)

            elif currCmd['type'] == AutoStepTypes.WAIT:
                logging.info("*** Wait ***")

            if 'delay' in currCmd:
                logging.info("*** Next Cmd in ~%is ***" % currCmd['delay'])

    def __unfold_loop(self):
        self.__appendCommands()
        self.loopListCurr[self.loopEntryCurr] = self.loopListCurr[self.loopEntryCurr]+1
        if self.loopListCurr[self.loopEntryCurr] >= self.loopCounts[self.loopEntryCurr]:
            while self.loopListCurr[self.loopEntryCurr] >= self.loopCounts[self.loopEntryCurr]:
                if self.loopEntryCurr == 0:
                    return False
                self.loopListCurr[self.loopEntryCurr] = 0
                self.loopEntryCurr = self.loopEntryCurr - 1
                self.loopListCurr[self.loopEntryCurr] = self.loopListCurr[self.loopEntryCurr]+1
            self.loopEntryCurr = len(self.loopCounts) -1
            return True
        else:
            return True

    def __appendCommands(self):
        logging.debug(self.loopListCurr)
        # defaults
        offType = "Button"
        offTimeMinutes = 15
        onDelaySeconds = 3

        # data for current loop state
        for loopNum in range(len(self.loops)):
            currLoop = self.loops[loopNum]
            if currLoop['type'] == 'offTime':
                offTimeMinutes = currLoop['values'][self.loopListCurr[loopNum]]['minutes']
            elif currLoop['type'] == 'offType':
                offType = currLoop['values'][self.loopListCurr[loopNum]]['type']
                if offType not in ['Button', 'Power']:
                    raise Exception('Unknown (off) type in: %s' % currLoop)
            elif currLoop['type'] == 'onDelayType':
                onDelaySeconds = currLoop['values'][self.loopListCurr[loopNum]]['seconds']

        # build commandlist
        self.commandList.append({ 'type': AutoStepTypes.INFO, 'msg': 'OnDelay: %i' % onDelaySeconds + ' / OffType: ' + offType + ' / OffTime: %i' % offTimeMinutes} )
        self.commandList.append({ 'type': AutoStepTypes.POWER_ON, 'delay': onDelaySeconds } )
        self.commandList.append({ 'type': AutoStepTypes.PUSH_BUTTON, 'delay': self.buttonPressSeconds } )
        self.commandList.append({ 'type': AutoStepTypes.WAIT, 'delay': self.onTimeSeconds } )
        if offType == "Button":
            self.commandList.append({ 'type': AutoStepTypes.PUSH_BUTTON, 'delay': self.buttonPressSeconds } )
            self.commandList.append({ 'type': AutoStepTypes.WAIT, 'delay': self.powerOffDelaySeconds } )
            self.commandList.append({ 'type': AutoStepTypes.POWER_OFF, 'delay': 0 } )
        else:
            self.commandList.append({ 'type': AutoStepTypes.POWER_OFF, 'delay': self.powerOffDelaySeconds } )
        self.commandList.append({ 'type': AutoStepTypes.WAIT, 'delay': offTimeMinutes * 60} )
        #self.commandList.append({ 'type': AutoStepTypes.WAIT, 'delay': offTimeMinutes} )
