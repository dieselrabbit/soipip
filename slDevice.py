
class slDevice:
    def __init__(self, slBridge, dataID, data):
        self.__bridge = slBridge
        self.__id = dataID
        self.__name = data["name"]
        self.__state = data["state"]
        self.__hassType = data["hassType"]

    def update(self, data):
        self.__state = data["state"]

    def id(self):
        return self.__id

    def name(self):
        return self.__name

    def state(self):
        return self.__state

    def hassType(self):
        return self.__hassType

    def toString(self):
        return "{}: {}".format(self.__name, self.__state)
