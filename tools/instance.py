import re
import ipaddress
from tools import nslookup

def determine_if_ip_or_endpoint(host):

    ec2_search_string = 'compute.amazonaws.com'
    rds_search_string = 'rds.amazonaws.com'

    if valid_ip(host):
        if is_public_ip(host):
            return "IP"
        else:
            return "Private IP"
    elif re.search(ec2_search_string, host) or re.search(rds_search_string, host):

        endpoint_validate = nslookup.name_to_ip(host)
        if endpoint_validate[0] == 1:
            return "Endpoint"
        else:

            return "Invalid Endpoint"

    elif not re.search(ec2_search_string, host) or not re.search(rds_search_string, host):
        return "Custom Endpoint"

    elif not valid_ip(host):
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

    elif not re.search(ec2_search_string, host) or not re.search(rds_search_string, host):

        endpoint = host

        ip = nslookup.name_to_ip(endpoint)

        arr3 = ip[1][3]

        if type(arr3) is str:

            ip = ip[1][3]
            print(ip)

            ip = ip.replace('Address: ', '')
            ip = ip.strip()

            print(ip)

            endpoint = nslookup.ip_to_name(ip)

            if re.search(ec2_search_string, endpoint):
                instance_type = 'EC2'
            elif re.search(rds_search_string, endpoint):
                instance_type = 'RDS'
            else:
                instance_type = 'Not a valid AWS resource'

        elif type(arr3) is list:

            arr = ip[1][3]

            pub_ip = []

            for i in range(len(arr)):
                # Searches for a valid ipV4
                found_ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', arr[i])

                if found_ip is not None:
                    pub_ip.append(found_ip.group())

            first_ipv4_ip = pub_ip[0]

            endpoints = nslookup.ip_to_name(first_ipv4_ip)

            if re.search(ec2_search_string, endpoints):
                instance_type = 'EC2'
            elif re.search(rds_search_string, endpoints):
                instance_type = 'RDS'
            else:
                instance_type = 'Not a valid AWS resource'

            return instance_type

        return instance_type
    elif re.search(ec2_search_string, host):
        instance_type = 'EC2'
    elif re.search(rds_search_string, host):
        instance_type = 'RDS'
    else:
        instance_type = 'Not a valid AWS resource'

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

