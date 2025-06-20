import unittest
from src.browser import URL

class URLTest(unittest.TestCase):

    def test_ctor_empty_url(self):
        undertest=URL("")
        self.assertEqual("file", undertest.scheme)
        self.assertEqual("/home/josh/jbrowser/tests/resources/simple.html", undertest.path)

    def test_ctor_no_url(self):
        undertest=URL()
        self.assertEqual("file", undertest.scheme)
        self.assertEqual("/home/josh/jbrowser/tests/resources/simple.html", undertest.path)

    def test_ctor_http_example_org(self):
        url = "http://example.org"
        undertest=URL(url)
        self.assertEqual("http", undertest.scheme)
        self.assertEqual(80, undertest.port)
        self.assertEqual("example.org", undertest.host)
        self.assertEqual("/", undertest.path)

    def test_ctor_nonstandard_port(self):
        url = "http://localhost:8080"
        undertest=URL(url)
        self.assertEqual("http", undertest.scheme)
        self.assertEqual(8080, undertest.port)
        self.assertEqual("localhost", undertest.host)
        self.assertEqual("/", undertest.path)

    def test_ctor_https_example_org(self):
        url = "https://example.org"
        undertest=URL(url)
        self.assertEqual("https", undertest.scheme)
        self.assertEqual(443, undertest.port)
        self.assertEqual("example.org", undertest.host)
        self.assertEqual("/", undertest.path)

    def test_ctor_https_iana_org_with_path(self):
        url = "https://www.iana.org/help/example-domains"
        undertest=URL(url)
        self.assertEqual("https", undertest.scheme)
        self.assertEqual(443, undertest.port)
        self.assertEqual("www.iana.org", undertest.host)
        self.assertEqual("/help/example-domains", undertest.path)

    def test_ctor_local_file(self):
        url = "file:///c/test/simple.html"
        undertest=URL(url)
        self.assertEqual("file", undertest.scheme)
        self.assertEqual("/c/test/simple.html", undertest.path)

    def test_request_local_file(self):
        url = "file:///home/josh/projects/jbrowser/tests/resources/simple.html"
        undertest=URL(url)
        result=undertest.request()
        self.assertEqual("<html><body><p>Hello, World!</p></body></html>", result)

    def test_ctor_data(self):
        url = "data:///text/html,Hello, World!"
        undertest=URL(url)
        self.assertEqual("data", undertest.scheme)

    def test_request_data(self):
        url = "data:///text/html,Hello, World!"
        undertest=URL(url)
        result=undertest.request()
        self.assertEqual("Hello, World!", result)

    # def test_show_entities(self):
    #     url = "data:///text/html,Hello, World"
    #     undertest=URL(url)
    #     body="&lt;div&gt;"
    #     result=undertest.show(body)
    #     self.assertEqual("<div>", result)

if __name__ == '__main__':
    unittest.main()