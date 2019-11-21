import subprocess
import re
from checkmate import instance

def name_to_ip(address):
    # Run command, for Endpoint to determine if it resolves to IP
    output = subprocess.run(['nslookup', address], capture_output=True, text=True)
    # Store output
    before_parsing = output.stdout
    # Take output and store in array
    before_parsing_arr = before_parsing.split('\n')
    # Output has spaces, this is an array to store spaces
    parsed_arr = []

    # Loop through output array and check for spaces, then add
    # elements to new array
    for i in range(len(before_parsing_arr)):
        if before_parsing_arr[i] != '':
            parsed_arr.append(before_parsing_arr[i])

    if len(parsed_arr) != 2:
        if 'Addresses' in parsed_arr[3]:
            addresses = []
            for i in range(3, len(parsed_arr)):
                address = parsed_arr[i]
                if "Addresses" in parsed_arr[i]:
                    address = address.replace("Addresses:", " ")
                    address = address.strip()
                else:
                    address = address.strip()
                addresses.append(address)

            sliced_arr = parsed_arr[slice(3)]
            sliced_arr.append(addresses)

            return 1, sliced_arr, before_parsing

        else:
            return 1, parsed_arr, before_parsing

    return 0, "Cannot find " + address + ", Non-existent domain"

def ip_to_name(ip_addr):

    command = 'nslookup'
    output = subprocess.run([command, ip_addr], capture_output=True, text=True)

    before_parsing = output.stdout

    before_parsing_arr = before_parsing.split('\n')

    parsed_arr = []

    for i in range(len(before_parsing_arr)):
        if before_parsing_arr[i] != '':
            parsed_arr.append(before_parsing_arr[i])

    name_element = ''
    for j in range(len(parsed_arr)):
        if re.search('Name:', parsed_arr[j]):
            name_element = parsed_arr[j]

    name_element = name_element.replace('Name: ', '')
    name_element = name_element.strip()

    return name_element

def get_default_gateway(ip_addr):

    command = 'nslookup'
    output = subprocess.run([command, ip_addr], capture_output=True, text=True)

    before_parsing = output.stdout

    before_parsing_arr = before_parsing.split('\n')

    parsed_arr = []

    for i in range(len(before_parsing_arr)):
        if before_parsing_arr[i] != '':
            parsed_arr.append(before_parsing_arr[i])

    default_gateway = parsed_arr[1]
    default_gateway = default_gateway.replace('Address: ', '')
    default_gateway = default_gateway.strip()

    return default_gateway
