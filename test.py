import unittest
import bs4
from pagecreeper import *;

class PageCreeperTest(unittest.TestCase):
    """test PageCreeper class functions"""

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




if __name__ == "__main__":
    unittest.main()
