import json


class BusinessUnit():
    '''
     the BusinessUnit class is used to describe the relationship of
     vulnerability and device
    '''

    name = ''
    itemIndex = ''
    lenovoCode = ''
    productList = []

    def __init__(self, name, lenovoCode, itemIndex):
        self.name = name
        self.lenovoCode = lenovoCode
        self.itemIndex = itemIndex

    def addDevice(self, deviceName):
        self.productList.append(deviceName)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
