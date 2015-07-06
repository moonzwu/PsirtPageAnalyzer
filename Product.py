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

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)