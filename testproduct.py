import unittest
from product import Product

class TestProduct(unittest.TestCase):
    '''
        test the product class behavior
    '''

    def test_deal_with_the_special_character_during_init(self):
        p = Product('EBG', 'TD350', 'Not affected', 'v1.0.0', '-')
        self.assertEqual(p.downloadLink, '')

    def test_there_is_no_fixversion_and_download_link_case(self):
        p = Product('EBG', 'TD350', 'Not affected', None, None)
        self.assertEqual(p.fixedVersion, '')
        self.assertEqual(p.downloadLink, '')

if __name__ == "__main__":
    unittest.main()