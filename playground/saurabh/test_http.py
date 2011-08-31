import unittest
import httplib2

def get(url):
    try:
        httplib2.Http().request(url, "GET")
        return True
    except Exception as e:
        return False
    
class TestHttp(unittest.TestCase):
    def test_localhost(self):
        url = "http://localhost"
        self.assertTrue(get(url), "Couldn't get %s" % url)
    
    def test_ys6(self):
        url = "http://yoursoft06.cs.rmit.edu.au"
        self.assertTrue(get(url), "Couldn't get %s" % url)
        
    def test_google(self):
        url = "http://www.google.com"
        self.assertTrue(get(url), "Couldn't get %s" % url)
    
if __name__ == '__main__':
    unittest.main()