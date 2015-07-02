import requests
import bs4
import html2text
import re
from multiprocessing import Pool
from vulelement import VulnerabilityElement


lenovoSupportHome = 'http://support.lenovo.com'
severityFlag = 'Severity:'
cveRep = r'CVE-\d{4}-\d{4}'

vulCollection = {}


def clearStr(inputStr):
    if (inputStr is None):
        return ''
    else:
        # print(inputStr.encode('utf-8'))
        return inputStr.replace('\n', '').replace('\\xa0', '').replace(':', '').strip()

def extractCVEcode(contentText):
    return re.findall(cveRep, contentText, re.M|re.I)


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

    #skip the table header line
    for index in range(1, len(items)):
        parseVulRow(items[index])

def parseVulDetail(lenovoCode, content):
    contentText = html2text.html2text(content.get_text()) # convert to pure text
    startPos = contentText.find(severityFlag)
    endPos   = contentText.find(' ', startPos + len(severityFlag) + 1)
    severity = contentText[startPos + len(severityFlag) + 1 : endPos]
    vulCollection[lenovoCode].severity = severity

    cveCodes = extractCVEcode(contentText)
    vulCollection[lenovoCode].cveCodes = repr(cveCodes)


def loadContentPage(url):
    print("loading " + url)
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)
    content = soup.select('div.content-wrapper')[0]
    return content

def processDetailPage(vul):
    content = loadContentPage(vul.link)
    parseVulDetail(vul.lenovoCode, content)

if __name__ == '__main__' :
    homeContent = loadContentPage('http://support.lenovo.com/us/en/product_security')
    parseVulTable(homeContent.table)

    # go though all vulnerability element
    pool = Pool(16)
    values = vulCollection.values()
    pool.map(processDetailPage, values)
    pool.close()
    pool.join()

    for vul in vulCollection.values():
        print(vulCollection[vul.lenovoCode].to_json())
