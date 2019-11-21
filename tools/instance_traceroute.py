import subprocess
from sys import platform as _platform
from tools import instance_nslookup as nslookup
import re
from checkmate import instance

def trace_route_of_instance(destination):
    if _platform == "linux" or _platform == "linux2":
        output = subprocess.run(['traceroute', destination], capture_output=True, text=True)
        return parse_output(output, destination)

    elif _platform == "darwin":
        print("Mac")

    elif _platform == "win32":
        output = subprocess.run(['tracert', destination], capture_output=True, text=True)
        return parse_output(output, destination)

    elif _platform == "win64":
        output = subprocess.run(['tracert', destination], capture_output=True, text=True)
        return parse_output(output, destination)

def parse_output(output, destination):
    before_parsing_arr = output.stdout
    before_parsing_arr = before_parsing_arr.split('\n')
    if before_parsing_arr[0] == 'Unable to resolve target system name ' + destination + '.':
        print("Fail")
    else:
        parsed_arr = []
        # Loop through output array and check for spaces, then add
        # elements to new array
        for i in range(len(before_parsing_arr)):
            if before_parsing_arr[i] != '':
                parsed_arr.append(before_parsing_arr[i])

        # Print parsed output
        for i in range(len(parsed_arr)):
            print(parsed_arr[i])

        traceroute_result = analyse_trace_route(destination, parsed_arr)

        return traceroute_result, parsed_arr

def analyse_trace_route(endpoint, parsed_output_arr):

    # Check first element to see whether it has the same default gateway
    # as a reverse nslookup would return (on a network other than AWS)
    is_first_hop = is_first_hop_default_gateway(endpoint, parsed_output_arr)

    # loop through check if it reaches a public IP, if it does break the loop and return True or 1
    found_public_ip = find_public_ip_in_trace(parsed_output_arr)

    # Check the last element to see if it is the same as the resolved ip for the given endpoint
    is_ip_same = is_ip_same_as_final_hop_in_trace(endpoint, parsed_output_arr)

    if is_first_hop and found_public_ip and is_ip_same:
        return "Traceroute Successful"
    elif is_first_hop and not found_public_ip:
        return "Reached Internet but not AWS Network"
    else:
        return "Traceroute unsuccessful"

def is_first_hop_default_gateway(endpoint, parsed_output_arr):

    # perform an nslookup on loopback (get ip from loopback response)
    local_default_gw = nslookup.get_default_gateway('127.0.0.1')
    print(local_default_gw)

    # check if the ip returned from loopback is in the first element of the array
    # if in then conclude the ip could make it through
    first_element = parsed_output_arr[2]

    if re.search(local_default_gw, first_element):
        return True
    else:
        return False

def find_public_ip_in_trace(parsed_output_arr):

    # find all valid ips in array (parse output further and extract all ips)
    valid_ip = []

    for i in range(len(parsed_output_arr)):

        found_ip = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', parsed_output_arr[i])
        if found_ip is not None:
            valid_ip.append(found_ip.group())

    # loop through each array element while checking if valid (instance.is_public_ip)
    idx = 0
    keep_looping = True
    while keep_looping:
        # once a valid public ip is found, break out of loop and return true
        if instance.is_public_ip(valid_ip[0]):
            keep_looping = False
            return True
        else:
            return False

def is_ip_same_as_final_hop_in_trace(endpoint, parsed_output_arr):

    ip = nslookup.name_to_ip(endpoint)
    ip = ip[1][3]
    ip = ip.replace('Address:', '')
    ip = ip.strip()

    ip_in_traceroute = parsed_output_arr[len(parsed_output_arr) - 2]

    if re.search(ip, ip_in_traceroute):
        return True
    else:
        return False





