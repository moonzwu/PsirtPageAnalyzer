import requests
import bs4
from vulelement import VulnerabilityElement

lenovoSupportHome = 'http://support.lenovo.com'


def clearStr(inputStr):
    return repr(inputStr.replace('\n', '')
                        .replace('\\xa0', '')
                        .replace(':', '')
                        .strip())


def parseRow(tableRow):
    lenovoCode  = ''
    description = ''
    link        = ''
    firstDate   = ''
    lastDate    = ''

    tdElems     = tableRow.find_all('td')
    strs        = list(tdElems[0].strings)
    lenovoCode  = clearStr(strs[0])
    description = clearStr(strs[1])

    aElems  = tdElems[0].find_all('a')
    link    = lenovoSupportHome + aElems[0]['href']

    firstDate   = clearStr(tdElems[1].string)
    lastDate    = clearStr(tdElems[2].string)

    ve = VulnerabilityElement(lenovoCode, description,
        link, firstDate, lastDate)
    print(ve.to_json())


response = requests.get('http://support.lenovo.com/us/en/product_security')
soup = bs4.BeautifulSoup(response.text)
content = soup.select('div.content-wrapper')[0]
table = content.table
items = table.find_all('tr')
for index in range(1, len(items)):
    parseRow(items[index])
