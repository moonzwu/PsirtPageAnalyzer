import unittest
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

if __name__ == "__main__":
    unittest.main()
