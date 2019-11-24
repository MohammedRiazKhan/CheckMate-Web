import unittest
from tools import traceroute

class TracerouteTestCase(unittest.TestCase):
    def test_successful_traceroute_with_4_hops(self):
        arr = traceroute.trace_route_of_instance('127.0.0.1')
        last_element = arr[len(arr)-1]
        self.assertTrue('Trace complete.' in last_element)

    def test_unsuccessful_traceroute_with_4_hops(self):
        arr = traceroute.trace_route_of_instance('127.0.0.0')
        self.assertTrue('failure.' in arr[1][1])

if __name__ == '__main__':
    unittest.main()
