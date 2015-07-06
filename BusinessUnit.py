import json

class BusinessUnit():
    '''
     the BusinessUnit class is used to describe the relationship of
     vulnerability and device
    '''

    name        = ''
    lenoveCode  = ''
    deviceList  = []

    def __init__(self, name, lenovoCode):
        self.name = name
        self.lenoveCode = lenovoCode

    def addDevice(self, deviceName):
        self.deviceList.append(deviceName)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
