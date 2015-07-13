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
        bu = BusinessUnit('ThinkServer & Storage', '000b1675_f972_494d_903d_22379095ac7a_0_3')
        products = parseProductsDetail(bu, productsBlockList)
        self.assertEqual(len(products), 17)
        self.assertEqual(products[0].name, 'ThinkServer    RD330')

    def test_get_products_in_the_software_category(self):
        soup = self.createSoupByTestFile('testdata/S3.htm')
        productsBlockList = soup.find_all('div', id='NewTileListContent')
        bu = BusinessUnit('Software', '000b1675_f972_494d_903d_22379095ac7a_1_1')
        products = parseProductsDetail(bu, productsBlockList)
        self.assertEqual(len(products), 9)
        self.assertEqual(products[1].name, 'Diagnostic')

    def test_get_products_with_four_columns_detail(self):
        soup = self.createSoupByTestFile('testdata/row_hammer.htm')
        productsBlockList = soup.find_all('div', id='NewTileListContent')
        bu = BusinessUnit('ThinkServer & Storage', 'b9e59df4_ac35_4a8d_848b_576f6d9c3939_0_3')
        products = parseProductsDetail(bu, productsBlockList)
        self.assertEqual(len(products), 22)
        self.assertEqual(products[0].name, 'ThinkServer RD330')
        self.assertEqual(products[0].status, 'Affected')
        self.assertEqual(products[0].fixedVersion, 'BIOS v9.4')
        self.assertEqual(products[0].downloadLink,
                         'http://support.lenovo.com/us/en/products/servers/thinkserver-rack-servers/thinkserver-rd330')

    def test_deal_with_the_no_BU_items_page(self):
        soup = self.createSoupByTestFile()
        contentNum = len(soup.select('div.content-wrapper'))
        self.assertEqual(1, contentNum)

    def test_update_products_to_BU(self):
        products =[]
        products.append(Product('ThinkServer', 'RD530', '-', '-'))
        products.append(Product('ThinkServer', 'RD430', '-', '-'))
        products.append(Product('ThinkServer', 'RD330', '-', '-'))
        bu = BusinessUnit('ThinkServer', 'b9e59df4_ac35_4a8d_848b_576f6d9c3939_0_3')
        buildRelationShipInVulBUProd(bu, products, '')
        self.assertEqual(len(bu.productCodeList), 3)
        self.assertEqual(bu.productCodeList[0], 'RD530')

if __name__ == "__main__":
    unittest.main()
