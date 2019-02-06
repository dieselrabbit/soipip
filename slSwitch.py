from constants import *
from slDevice import slDevice

class slSwitch(slDevice):
    def __init__(self, slBridge, dataID, data):
        if('hassType' not in data):
            data['hassType'] = "switch"
        super().__init__(slBridge, dataID, data)

    def toggle(self):
        if(state == 0):
            newState = 1
        else:
            newState = 0
        
        if(self.__bridge.setCircuit(self.__id, newState)):
            print("{} set to {}".format(self.__name, self.stateText()))
        else:
            print("Setting of circuit failed!")

    def isOn(self):
        if(state == 1):
            return True
        else:
            return False

    def stateText(self):
        return mapping.ON_OFF[self.__state]
