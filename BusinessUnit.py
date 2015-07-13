import json


class BusinessUnit():
    '''
     the BusinessUnit class is used to describe the relationship of
     vulnerability and device
    '''

    name = '' # unique key
    itemIndex = ''
    productCodeList = []

    def __init__(self, name, itemIndex):
        self.name = name
        self.itemIndex = itemIndex

    def addDevice(self, deviceName):
        self.productCodeList.append(deviceName)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
