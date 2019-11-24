import unittest
from tools import telnet

class TelnetTestCase(unittest.TestCase):
    def test_telnet_with_port_open(self):
        response = telnet.check_if_port_open('127.0.0.1', 3306)
        self.assertEqual(response[0], 1)

    def test_telnet_with_port_closed(self):
        response = telnet.check_if_port_open('127.0.0.1', 1511)
        self.assertEqual(response[0], 0)

if __name__ == '__main__':
    unittest.main()
