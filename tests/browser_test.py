import unittest
from src.browser import Browser

class URLTest(unittest.TestCase):

    def test_ctor(self):
        undertest=Browser()
        
        self.assertEqual(800, undertest.width)
        self.assertEqual(600, undertest.height)
        self.assertEqual(0, undertest.max_x)
        self.assertEqual(0, undertest.max_y)
        self.assertEqual(0, undertest.scroll_x)
        self.assertEqual(0, undertest.scroll_y)
        self.assertEqual(False, undertest.issource)

    def test_issource(self):
        undertest=Browser()
        undertest.show_src()
        self.assertEqual(True, undertest.issource)

if __name__ == '__main__':
    unittest.main()