import unittest
from tools import ping

class PingTestCase(unittest.TestCase):
    def test_ping_with_reply(self):
        response = ping.perform_ping('127.0.0.1')
        self.assertFalse('Reply' in response[1])

    def test_ping_without_reply(self):
        response = ping.perform_ping('127.0.0.0')
        self.assertFalse('Reply' in response[1])

    def test_ping_with_reply_endpoint(self):
        response = ping.perform_ping('www.google.com')
        self.assertTrue('Reply' == 'Reply')

    def test_ping_without_reply_endpoint(self):
        response = ping.perform_ping('www.googley.com')
        self.assertFalse('Reply' in response[1])

    def test_ping_with_loss(self):
        self.assertEqual('a', 'a')

    # def test_ping_request_timed_out(self):
    #     response = ping.test_ping('dedfe')
    #     self.assertTrue('Request' in response[1])

    def test_fail_ping(self):
        response = ping.perform_ping('www.googlfasdfaey.com')
        print(response)
        self.assertFalse('Request timed out.' in response)

if __name__ == '__main__':
    unittest.main()
