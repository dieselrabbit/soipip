from slDevice import slDevice

class slSensor(slDevice):
    def __init__(self, slBridge, dataID, data):
        if('hassType' not in data):
            data['hassType'] = "sensor"
        super().__init__(slBridge, dataID, data)
        if('unit' in data):
            self.__unit = data["unit"]
        else:
            self.__unit = ""

    def getUnit(self):
        return self.__unit

    def getValue(self):
        return self.__state
