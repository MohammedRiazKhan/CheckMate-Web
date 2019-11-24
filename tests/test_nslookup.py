import unittest
from tools import nslookup

class NslookupTest(unittest.TestCase):

    def test_nslookup(self):
        state = nslookup.name_to_ip('amazon.com')
        self.assertNotEqual(state, None)

    def test_ip_to_name(self):
        ip = '3.10.62.33'
        endpoint = 'ec2-3-10-62-33.eu-west-2.compute.amazonaws.com'
        result = nslookup.ip_to_name(ip)
        self.assertEqual(result, endpoint)

    def test_invalid_endpoint(self):
        endpoint = 'glaksfdjglas/.com'
        result = nslookup.name_to_ip(endpoint)
        # if the response code is equal (0=failure, 1=success)
        self.assertEqual(result[0], 0)


if __name__ == '__main__':
    unittest.main()
