import sys
import time
from multiprocessing import Lock
from discoverGateway import discoverGateway
from slConnection import slConnection
from doQuery import queryGateway, queryConfig, queryStatus, queryButtonPress

class slBridge:
    def __init__(self, verbose=False, updateInterval=30, gatewayIP=None, gatewayPort=None):
        self.__lastUpdate = 0
        self.__updateInterval = updateInterval
        self.__lock = Lock()
        self.__data = {}
        self.__circuits = {}
        
        if(not gatewayIP):
              gatewayIP, gatewayPort, gatewayType, gatewaySubtype, \
              gatewayName, okchk = discoverGateway(verbose)

        if(gatewayIP):
            connection = slConnection()
            if(connection.connect(gatewayIP, gatewayPort)):
                self.connection = connection
                if(verbose):
                    print("connection success!")
                self.update()
            else:
                if(verbose):
                    print("connection failed!")

    def update(self):
        curTime = time.time()
        with self.__lock:
            if ((curTime - self.__lastUpdate) > self.__updateInterval):
                self.__lastUpdate = curTime
                self.__data['config'] = queryConfig(self.connection)
                self.__data['states'] = queryStatus(self.connection)
                for i in self.__data['config']['circuits']['data']:
                    cID = '%s' % i['id']
                    self.__circuits[cID] = {}
                    self.__circuits[cID]['id'] = cID
                    self.__circuits[cID]['name'] = self.__data['config']['circuits']['names'][cID]
                    self.__circuits[cID]['state'] = self.__data['states']['circuits']['states'][cID]
                    #print(self.__circuits[cID])

    def getConfig(self):
        return self._data['config']

    def getStates(self):
        return self.__data['states']

    def getCircuits(self):
        return self.__circuits

    def getChemistry(self):
        return self.__data['states']['chemistry']

    def setCircuit(self, circuitID, circuitState):
        print(queryButtonPress(self.connection, circuitID, circuitState))

        
if __name__ == "__main__":
    bridge = slBridge(False)
    if(len(sys.argv) > 1):
        if(sys.argv[1] == 'circuits'):
            print(bridge.getCircuits())
        elif(sys.argv[1] == 'chemistry'):
            print(bridge.getChemistry())
        elif(sys.argv[1] == 'setCircuit'):
            if(len(sys.argv) == 4):
                print(bridge.setCircuit(sys.argv[2], sys.argv[3]))
        else:
            print("Unknown option!")
    else:
        print(bridge.getCircuits())
        print(bridge.getStates())
    #bridge.connection.socket.close()
