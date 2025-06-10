import unittest
from src.browser import URL

class URLTest(unittest.TestCase):

    def test_ctor_empty_url(self):
        browser=URL("")
        self.assertEqual("file", browser.scheme)
        self.assertEqual("/home/josh/jbrowser/tests/resources/simple.html", browser.path)

    def test_ctor_no_url(self):
        browser=URL()
        self.assertEqual("file", browser.scheme)
        self.assertEqual("/home/josh/jbrowser/tests/resources/simple.html", browser.path)

    def test_ctor_http_example_org(self):
        url = "http://example.org"
        browser=URL(url)
        self.assertEqual("http", browser.scheme)
        self.assertEqual(80, browser.port)
        self.assertEqual("example.org", browser.host)
        self.assertEqual("/", browser.path)

    def test_ctor_nonstandard_port(self):
        url = "http://localhost:8080"
        browser=URL(url)
        self.assertEqual("http", browser.scheme)
        self.assertEqual(8080, browser.port)
        self.assertEqual("localhost", browser.host)
        self.assertEqual("/", browser.path)

    def test_ctor_https_example_org(self):
        url = "https://example.org"
        browser=URL(url)
        self.assertEqual("https", browser.scheme)
        self.assertEqual(443, browser.port)
        self.assertEqual("example.org", browser.host)
        self.assertEqual("/", browser.path)

    def test_ctor_https_iana_org_with_path(self):
        url = "https://www.iana.org/help/example-domains"
        browser=URL(url)
        self.assertEqual("https", browser.scheme)
        self.assertEqual(443, browser.port)
        self.assertEqual("www.iana.org", browser.host)
        self.assertEqual("/help/example-domains", browser.path)

    def test_ctor_local_file(self):
        url = "file:///c/test/simple.html"
        browser=URL(url)
        self.assertEqual("file", browser.scheme)
        self.assertEqual("/c/test/simple.html", browser.path)

    def test_request_local_file(self):
        url = "file:///home/josh/jbrowser/tests/resources/simple.html"
        browser=URL(url)
        result=browser.request()
        self.assertEqual("<html><body><p>Hello, World!</p></body></html>", result)

    def test_ctor_data(self):
        url = "data:///text/html,Hello, World!"
        browser=URL(url)
        self.assertEqual("data", browser.scheme)

    def test_request_data(self):
        url = "data:///text/html,Hello, World!"
        browser=URL(url)
        result=browser.request()
        self.assertEqual("Hello, World!", result)

if __name__ == '__main__':
    unittest.main()