import requests
import bs4
from vulelement import VulnerabilityElement

lenovoSupportHome = 'http://support.lenovo.com'
severityFlag = 'Severity:'

vulCollection = {}


def clearStr(inputStr):
    if (inputStr is None):
        return ''
    else:
        # print(inputStr.encode('utf-8'))
        return repr(inputStr.replace('\n', '')
                        .replace('\\xa0', '')
                        .replace(':', '')
                        .strip())


def parseVulRow(tableRow):
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
    #print(ve.to_json())
    vulCollection[lenovoCode] = ve


def parseVulTable(vulTable):
    items = vulTable.find_all('tr')
    for index in range(1, len(items)):
        parseVulRow(items[index])

def parseVulDetail(lenovoCode, content):
    pElems = content.find_all('p')
    pContent = pElems[1]
    contentText = pContent.get_text()
    startPos = contentText.find(severityFlag)
    endPos   = contentText.find('\n\n', startPos)
    severity = contentText[startPos + len(severityFlag) + 1 : endPos]
    vulCollection[lenovoCode].severity = severity

    ulElems = content.find_all('ul')
    cveCode = clearStr(ulElems[1].li.string)
    vulCollection[lenovoCode].cveCode = cveCode


def loadContentPage(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)
    content = soup.select('div.content-wrapper')[0]
    return content



homeContent = loadContentPage('http://support.lenovo.com/us/en/product_security')
parseVulTable(homeContent.table)

# go though all vulnerability element
for vul in vulCollection.values():
    content = loadContentPage(vul.link)
    parseVulDetail(vul.lenovoCode, content)
    print(vulCollection[vul.lenovoCode].to_json())
