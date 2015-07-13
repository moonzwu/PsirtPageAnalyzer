import json


class Product():
    '''
        Product class is used to describe the each product of different BU
    '''
    buName = '' # foreign key to BU entity
    name = '' # unique key
    lenovoCode = ''
    status = ''
    fixedVersion = ''
    downloadLink = ''

    def __init__(self, buName, name, lenovoCode, status, fixedVersion='', downloadLink=''):
        self.buName = buName
        self.name = name
        self.lenovoCode = lenovoCode
        self.status = status
        self.fixedVersion = (fixedVersion is not None) and fixedVersion or ''
        self.downloadLink = (downloadLink is not None and downloadLink != '-') and downloadLink or ''

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
