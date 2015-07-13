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

    def test_get_products_by_BU_object(self):
        soup = self.createSoupByTestFile('testdata/S3.htm')
        productsBlockList = soup.find_all('div', id='NewTileListContent')
        bu = BusinessUnit('ThinkServer & Storage', 'LEN-2014-006', '000b1675_f972_494d_903d_22379095ac7a_0_3')
        products = parseProductsDetail(bu, productsBlockList)
        self.assertEqual(len(products), 17)
        self.assertEqual(products[0].name, 'ThinkServer    RD330')

    def test_get_products_in_the_software_category(self):
        soup = self.createSoupByTestFile('testdata/S3.htm')
        productsBlockList = soup.find_all('div', id='NewTileListContent')
        bu = BusinessUnit('Software', 'LEN-2014-006', '000b1675_f972_494d_903d_22379095ac7a_1_1')
        products = parseProductsDetail(bu, productsBlockList)
        self.assertEqual(len(products), 9)
        self.assertEqual(products[1].name, 'Diagnostic')


    def test_deal_with_the_no_BU_items_page(self):
        soup = self.createSoupByTestFile()
        contentNum = len(soup.select('div.content-wrapper'))
        self.assertEqual(1, contentNum)


if __name__ == "__main__":
    unittest.main()
