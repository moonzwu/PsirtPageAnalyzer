import json


class VulnerabilityElement():

    """ VulnerabilityElement
        is used to describe the vulnerability of Lenovo monitored
    """
    lenovoCode = ""
    description = ""
    link = ""
    firstPublishedDate = ""
    lastUpdatedDate = ""
    severity = ""
    cveCodes = ""

    def __init__(self, code, description, link, firstDate, lastDate):
        self.lenovoCode = code
        self.description = description
        self.link = link
        self.firstPublishedDate = firstDate
        self.lastUpdatedDate = lastDate

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
