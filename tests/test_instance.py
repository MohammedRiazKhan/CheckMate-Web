import unittest
from tools import instance

class InstanceTest(unittest.TestCase):

    def test_determine_instance_type_by_endpoint_ec2(self):
        host = 'ec2-35-177-190-236.eu-west-2.compute.amazonaws.com'
        instance_type = instance.determine_instance_type_by_endpoint(host)
        self.assertEqual(instance_type, "EC2")

    def test_determine_instance_type_by_endpoint_rds(self):
        host = 'checkmate-mssql.czrub0mfxuvk.eu-west-2.rds.amazonaws.com'
        instance_type = instance.determine_instance_type_by_endpoint(host)
        self.assertEqual(instance_type, "RDS")

    def test_determine_instance_type_by_endpoint_multiple_entries_ec2_first(self):
        host = 'ec2-35-177-190-236.eu-west-2.compute.amazonaws.com checkmate-mssql.czrub0mfxuvk.eu-west-2.rds.amazonaws.com'
        instance_type = instance.determine_instance_type_by_endpoint(host)
        self.assertEqual(instance_type, "EC2")

    def test_determine_instance_type_by_endpoint_multiple_entries_rds_first(self):
        host = 'checkmate-mssql.czrub0mfxuvk.eu-west-2.rds.amazonaws.com ec2-35-177-190-236.eu-west-2.compute.amazonaws.com'
        instance_type = instance.determine_instance_type_by_endpoint(host)
        self.assertEqual(instance_type, "RDS")

    def test_determine_if_ip_or_endpoint_when_ip_valid(self):
        host = '10.0.0.1'
        ip = instance.determine_if_ip_or_endpoint(host)
        self.assertEqual(ip, "IP")

    def test_determine_if_ip_or_endpoint_when_ip_invalid(self):
        host = '100.0.1'
        ip = instance.determine_if_ip_or_endpoint(host)
        self.assertEqual(ip, "Invalid IP")

    def test_determine_if_ip_or_endpoint_when_endpoint(self):
        host = 'ec2-35-177-190-236.eu-west-2.compute.amazonaws.com'
        ip = instance.determine_if_ip_or_endpoint(host)
        self.assertEqual(ip, "Endpoint")

    def test_determine_instance_type_by_ip(self):
        ip = '3.10.62.33'
        result = instance.determine_instance_type_by_ip(ip)
        self.assertEqual(result, "EC2")

    def test_is_public_ip(self):
        privaate_ip = '172.16.0.0'
        valid_ip = '52.25.26.45'
        res1 = instance.is_public_ip(privaate_ip)
        res2 = instance.is_public_ip(valid_ip)
        self.assertEqual(res1, False)
        self.assertEqual(res2, True)

if __name__ == '__main__':
    unittest.main()
