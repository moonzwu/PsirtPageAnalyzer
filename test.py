import unittest
import bs4
from pagecreeper import *;


class PageCreeperTest(unittest.TestCase):
    """test PageCreeper class functions"""

    def createSoupByTestFile(self, htmFile="testdata/lenovo_fpr.htm"):
        file = open(htmFile, "r")
        html = file.read()
        file.close()
        soup = bs4.BeautifulSoup(html)
        return soup

    def test_get_single_cvecode_from_page_content(self):
        contextText = 'Hello world CVE ID: CVE-2015-1170 I am working'
        cveCodes = extractCVEcode(contextText)
        self.assertEqual(len(cveCodes), 1)
        self.assertEqual(cveCodes[0], 'CVE-2015-1170')

    def test_get_multi_cvecodes_from_text(self):
        contextText = 'Hello world CVE ID: CVE-2015-1170,CVE-2015-1010 I am working '
        cveCodes = extractCVEcode(contextText)
        self.assertEqual(len(cveCodes), 2)

    def test_locate_the_item_by_BU_name(self):
        html = '''
                <li role="tab" aria-controls="tab_item-3" class="cell2 resp-tab-item" itemindex="84bca948_c26a_45e4_8ebb_fa1d8c759d19_0_3">
                    <div class="contactUs-tile gray-bg" style="height: 48px;">
                    <div class="fluid-row">
                    <div class="cell8 stack-fix contactUs-tile-label">ThinkServer &amp; Storage</div>
                    </div>
                    </div>
                </li>
                '''
        soup = bs4.BeautifulSoup(html)
        buName = 'ThinkServer & Storage'
        liElem = soup.select('li')[0]
        elem = liElem.find_all(text=buName)
        if elem is not None:
            index = liElem['itemindex']
            print(index)
        else:
            print(repr(elem))

    def test_get_products_by_BU_object(self):
        soup = self.createSoupByTestFile('testdata/S3.htm')
        productsBlock = soup.find_all('div', id='NewTileListContent')
        bu = BusinessUnit('ThinkServer & Storage', 'LEN-2014-006', '000b1675_f972_494d_903d_22379095ac7a_0_3')
        products = parseProductsDetail(bu, productsBlock[0])
        self.assertEqual(len(products), 17)
        self.assertEqual(products[0].name, 'ThinkServer    RD330')

    def test_deal_with_the_no_BU_items_page(self):
        soup = self.createSoupByTestFile()
        contentNum = len(soup.select('div.content-wrapper'))
        self.assertEqual(1, contentNum)


if __name__ == "__main__":
    unittest.main()
