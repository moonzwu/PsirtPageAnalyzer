import json


class Product():
    '''
        Product class is used to describe the each product of different BU
    '''
    buName = ''
    name = ''
    status = ''
    fixedVersion = ''
    downloadLink = ''

    def __init__(self, buName, name, status, fixedVersion='', downloadLink=''):
        self.buName = buName
        self.name = name
        self.status = status
        self.fixedVersion = (fixedVersion is not None) and fixedVersion or ''
        self.downloadLink = (downloadLink is not None and downloadLink != '-') and downloadLink or ''

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
