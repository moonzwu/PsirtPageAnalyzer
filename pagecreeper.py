import requests
import bs4
import html2text
import re
import logging
from requests.exceptions import *
from multiprocessing import Pool
from vulelement import VulnerabilityElement
from businessunit import BusinessUnit

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
    vulCollection[lenovoCode] = ve


def parseVulTable(vulTable):
    items = vulTable.find_all('tr')

    #skip the table header line
    for index in range(1, len(items)):
        parseVulRow(items[index])

def parseVulDetail(vul, content):
    contentText = html2text.html2text(content.get_text()) # convert to pure text
    startPos = contentText.find(severityFlag)
    endPos   = contentText.find(' ', startPos + len(severityFlag) + 1)
    severity = contentText[startPos + len(severityFlag) + 1 : endPos]
    vul.severity = severity

    cveCodes = extractCVEcode(contentText)
    vul.cveCodes = repr(cveCodes)
    #print(vul.to_json())

    parseBUDetail(vul.lenovoCode, content)


def parseBUDetail(lenovoCode, content):
    buList = []
    buAndProdsElem = content.find_all(id='NewTileListComponent')
    if buAndProdsElem is not None and len(buAndProdsElem) > 0:
        for ulElem in buAndProdsElem[0].find_all('ul'):
            for liElem in ulElem.find_all('li'):
                bu = BusinessUnit(liElem.get_text(), lenovoCode, liElem['itemindex'])
                buList.append(bu)
        print(len(buList))



def loadContentPage(url):
    print("loading " + url)
    for i in range(3):
        try:
            response = requests.get(url, timeout=30)
            soup = bs4.BeautifulSoup(response.text)
            content = soup.select('div.content-wrapper')[0]
            return content
        except (ReadTimeout, Timeout, ConnectTimeout):
            print("get a timeout exception")
            continue

def processDetailPage(vul):
    try:
        content = loadContentPage(vul.link)
        parseVulDetail(vul, content)
    except Exception:
        logging.exception("arg is %s" % vul.lenovoCode)

if __name__ == '__main__' :
    homeContent = loadContentPage('http://support.lenovo.com/us/en/product_security')
    parseVulTable(homeContent.table)

    # go though all vulnerability element
    pool = Pool(16)
    pool.map(processDetailPage, vulCollection.values())
    pool.close()
    pool.join()

    # for vul in vulCollection.values():
    #     print(vulCollection[vul.lenovoCode].to_json())
