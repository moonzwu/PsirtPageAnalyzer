import requests
import bs4
import html2text
import re
import logging
from requests.exceptions import *
from multiprocessing import Pool
from vulnerability import Vulnerability
from BusinessUnit import BusinessUnit
from Product import Product

lenovoSupportHome = 'http://support.lenovo.com'
severityFlag = 'Severity:'
cveRep = r'CVE-\d{4}-\d{4}'

vulCollection = {}


def clearSpecialChars(inputStr):
    if (inputStr is None):
        return ''
    else:
        # print(inputStr.encode('utf-8'))
        return inputStr.replace('\n', '').replace('\\xa0', '').replace(':', '').strip()


def extractCVEcode(contentText):
    return re.findall(cveRep, contentText, re.M | re.I)

def selectValidCVETextBlock(entireVulContent):
    lis = entireVulContent.find_all('li')
    for li in lis:
        validCVEContent = html2text.html2text(li.get_text())
        if (validCVEContent.find("CVE ID:") != -1):
            return validCVEContent

    # deal with the no <li> tag for CVE ID case
    vulTxtContent = html2text.html2text(entireVulContent.get_text())
    startPos = vulTxtContent.find("CVE ID:")
    if (startPos != -1):
        return vulTxtContent[startPos:]
    else:
        return ''

def parseVulRow(tableRow):
    tdElems = tableRow.find_all('td')
    strs = list(tdElems[0].strings)
    lenovoCode = clearSpecialChars(strs[0])
    description = clearSpecialChars(strs[1])

    aElems = tdElems[0].find_all('a')
    link = lenovoSupportHome + aElems[0]['href']

    firstDate = clearSpecialChars(tdElems[1].string)
    lastDate = clearSpecialChars(tdElems[2].string)

    ve = Vulnerability(lenovoCode, description,
                              link, firstDate, lastDate)
    vulCollection[lenovoCode] = ve


def parseVulTable(vulTable):
    items = vulTable.find_all('tr')

    # skip the table header line
    for index in range(1, len(items)):
        parseVulRow(items[index])


def parseVulDetail(vul, entireVulContent):
    pureTextOfContent = html2text.html2text(entireVulContent.get_text())  # convert to pure text
    startPos = pureTextOfContent.find(severityFlag)
    endPos = pureTextOfContent.find(' ', startPos + len(severityFlag) + 1)
    severity = pureTextOfContent[startPos + len(severityFlag) + 1: endPos]
    vul.severity = severity

    cveCodes = extractCVEcode(pureTextOfContent)
    vul.cveCodes = repr(cveCodes)
    # print(vul.to_json())

    buList = parseBUDetail(entireVulContent)

    # get the product list from each Business Unit
    productsContentBlockList = entireVulContent.find_all('div', id='NewTileListContent')
    for bu in buList:
        products = parseProductsDetail(bu, productsContentBlockList)
        buildRelationShipInVulBUProd(bu, products, vul.lenovoCode)


def buildRelationShipInVulBUProd(bu, products, lenovoCode):
    for product in products:
        bu.addDevice(product.name)
        product.lenovoCode = lenovoCode


def parseBUDetail(content):
    buList = []
    buAndProdsElem = content.find_all(id='NewTileListComponent')
    if buAndProdsElem is not None and len(buAndProdsElem) > 0:
        for ulElem in buAndProdsElem[0].find_all('ul'):
            for liElem in ulElem.find_all('li'):
                bu = BusinessUnit(liElem.get_text(), liElem['itemindex'])
                buList.append(bu)
    return buList


def parseProductsDetail(bu, productsContentBlockList):
    buProductsBlockList = []
    for productsContentBlock in productsContentBlockList:
        buProductsBlockList = productsContentBlock.find_all('div', itemindex=bu.itemIndex)
        if len(buProductsBlockList) != 0:
            break

    if len(buProductsBlockList) == 0:
        return []

    productsTable = buProductsBlockList[0].table
    productRowList = productsTable.find_all('tr')
    if len(productRowList) > 0:
        products = []
        for index in range(1, len(productRowList)):
            row = productRowList[index]
            columns = row.find_all('td')
            if len(columns) == 2:
                products.append(Product(bu.name, columns[0].get_text(),
                                        columns[1].get_text()))
            elif len(columns) == 4:
                products.append(Product(bu.name, columns[0].get_text(),
                                        columns[1].get_text(),
                                        columns[2].get_text(),
                                        columns[3].get_text()))
            else:
                pass
        return products
    else:
        return []

def loadContentPage(url):
    print("loading " + url)

    # try three times to avoid the timeout case
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
        entireVulContent = loadContentPage(vul.link)
        parseVulDetail(vul, entireVulContent)
    except Exception:
        logging.exception("arg is %s" % vul.lenovoCode)


if __name__ == '__main__':
    homeContent = loadContentPage('http://support.lenovo.com/us/en/product_security')
    parseVulTable(homeContent.table)

    # go though all vulnerability element
    pool = Pool(16)
    pool.map(processDetailPage, vulCollection.values())
    pool.close()
    pool.join()

    # for vul in vulCollection.values():
    #     print(vulCollection[vul.lenovoCode].to_json())
