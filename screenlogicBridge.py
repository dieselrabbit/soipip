import sys
import time
from multiprocessing import Lock
from discoverGateway import discoverGateway
from slGateway import slGateway
from doQuery import queryGateway, queryConfig, queryStatus, queryButtonPress
from slSwitch import slSwitch
from slSensor import slSensor

class slBridge:
    def __init__(self, verbose=False, updateInterval=30, gatewayIP=None, gatewayPort=None):
        self.__lastUpdate = 0
        self.__updateInterval = updateInterval
        self.__lock = Lock()
        self.__data = {}
        self.__devices = {}
        
        if(not gatewayIP):
              gatewayIP, gatewayPort, gatewayType, gatewaySubtype, \
              gatewayName, okchk = discoverGateway(verbose)

        if(gatewayIP):
            self.__gateway = slGateway(gatewayIP, gatewayPort)
            if(self.__gateway.connect()):
                if(verbose):
                    print("connection success!")
                self.update()
                self.__gateway.disconnect()
            else:
                if(verbose):
                    print("connection failed!")

    def update(self):
        curTime = time.time()
        with self.__lock:
            if ((curTime - self.__lastUpdate) > self.__updateInterval):
                self.__lastUpdate = curTime
                self._updateData()
                self._updateDevices()
                
    def _updateData(self):
        self.__gateway.getData(self.__data)

    def _updateDevices(self):
        self._updateSwitches()
        self._updateSensors()
        for k, d in self.__devices.items():
            print("{} - {}: {}".format(d.hassType, d.name, d.friendlyState))

    def _updateSwitches(self):
        for k, v in self.__data['circuits'].items():
            if('hassType' in v):
                if(k in self.__devices):
                    self.__devices[k].update(v)
                else:
                    self.__devices[k] = slSwitch(self, k, v)

    def _updateSensors(self):
        for k, v in self.__data['sensors'].items():
            if('hassType' in v):
                if(k in self.__devices):
                    self.__devices[k].update(v)
                else:
                    self.__devices[k] = slSensor(self, k, v)
        for i in self.__data['bodies']:
            for k, v in self.__data['bodies'][i].items():
                if('hassType' in v):
                    kI = "{}_{}".format(k, i)
                    if(kI in self.__devices):
                        self.__devices[kI].update(v)
                    else:
                        self.__devices[kI] = slSensor(self, kI, v)
        for k, v in self.__data['chemistry'].items():
            if('hassType' in v):
                if(k in self.__devices):
                    self.__devices[k].update(v)
                else:
                    self.__devices[k] = slSensor(self, k, v)


    #def _updateDevice(self, dataID, data):
    #    for d in self.__devices

    def getConfig(self):
        return self._data['config']

    def getChemistry(self):
        return self.__data['states']['chemistry']

    def setCircuit(self, circuitID, circuitState):
        if(circuitID in self.__devices and self.__gateway.setCircuit(circuitID, circuitState)):
            self._updateData()
            return True

        
if __name__ == "__main__":
    bridge = slBridge(True)
    #if(len(sys.argv) > 1):
    #    if(sys.argv[1] == 'circuits'):
    #        print(bridge.getCircuits())
    #    elif(sys.argv[1] == 'chemistry'):
    #        print(bridge.getChemistry())
    #    elif(sys.argv[1] == 'setCircuit'):
    #        if(len(sys.argv) == 4):
    #            print(bridge.setCircuit(sys.argv[2], sys.argv[3]))
    #    else:
    #        print("Unknown option!")
    #else:
    #    print(bridge.getCircuits())
    #    print(bridge.getStates())
    #bridge.connection.socket.close()
