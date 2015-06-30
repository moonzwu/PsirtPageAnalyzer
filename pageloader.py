import requests
import bs4

def parseRow(rowHtml):
    tdElems = rowHtml.find_all('td')
    for item in tdElems:
        print(item.get_text().encode('utf-8').decode('utf-8'))

    aElems = rowHtml.find_all('a')
    for a in aElems:
        print(a['href'])




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
    cveCode = ""

    def __init__(self, code, description, link, firstDate, lastDate):
        self.lenovoCode = code
        self.description = description
        self.link = link
        self.firstPublishedDate = firstDate
        self.lastUpdatedDate = lastDate



response = requests.get('http://support.lenovo.com/us/en/product_security')
soup = bs4.BeautifulSoup(response.text)
content = soup.select('div.content-wrapper')[0]
table = content.table
items = table.find_all('tr')
for index in range(1, len(items)):
    parseRow(items[index])
