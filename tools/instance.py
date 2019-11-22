import re
import ipaddress
from tools import nslookup

def determine_if_ip_or_endpoint(host):

    ec2_search_string = 'compute.amazonaws.com'
    rds_search_string = 'rds.amazonaws.com'

    if valid_ip(host):
        return "IP"
    if re.search(ec2_search_string, host) or re.search(rds_search_string, host):
        return "Endpoint"
    if not valid_ip(host):
        return "Invalid IP"

def valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def determine_instance_type_by_endpoint(host):
    instance_type = ''
    ec2_search_string = 'compute.amazonaws.com'
    rds_search_string = 'rds.amazonaws.com'

    if re.search(ec2_search_string, host) and re.search(rds_search_string, host):

        ec2_result = host.find(ec2_search_string)
        rds_result = host.find(rds_search_string)

        if ec2_result != -1 and rds_result != -1:
            if ec2_result < rds_result:
                instance_type = 'EC2'
            else:
                instance_type = 'RDS'

    elif re.search(ec2_search_string, host):
        instance_type = 'EC2'
    elif re.search(rds_search_string, host):
        instance_type = 'RDS'

    return instance_type


def determine_instance_type_by_ip(host):

    # Get endpoint
    endpoint = nslookup.ip_to_name(host)
    # Pass into this
    return determine_instance_type_by_endpoint(endpoint)


def is_public_ip(ip):
    if not ipaddress.ip_address(ip).is_private:
        return True
    else:
        return False



