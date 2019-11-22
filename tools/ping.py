import subprocess

def perform_ping(host):

    output = subprocess.run(['ping', host], capture_output=True, text=True)

    before_parsing = output.stdout

    parsed = before_parsing.split('\n')
    parsed_arr = []
    result_arr = []
    parsed_result = []

    for i in range(len(parsed)):
        if parsed[i] != '':
            parsed_arr.append(parsed[i])
            result_arr = parsed_arr[slice(6, 7)]

    if result_arr:
        parsed_result = result_arr[0].split(',')
        parsed_result.pop(3)

    for i in range(len(parsed_result)):
        parsed_result[i] = parsed_result[i].strip()
        if i == 0:
            parsed_result[i] = parsed_result[i].replace('Packets: Sent = ', '')
        if i == 1:
            parsed_result[i] = parsed_result[i].replace('Received = ', '')
        if i == 2:
            parsed_result[i] = parsed_result[i].replace('Lost = ', '')
            parsed_result[i] = parsed_result[i].replace(' (0% loss)', '')

    return analyse_ping(parsed_arr, parsed_result, host, before_parsing)

def analyse_ping(parsed_array, parsed_result, host, raw_output):

    count = 2
    request_time_out_count = 0
    destination_unreachable_count = 0

    if len(parsed_array) > 1:

        has_all_responses_extracted = [parsed_array[1], parsed_array[2], parsed_array[3], parsed_array[4]]
        for i in range(len(has_all_responses_extracted)):
            if has_all_responses_extracted[i] == 'Request timed out.':
                request_time_out_count += 1
        for i in range(len(has_all_responses_extracted)):
            if has_all_responses_extracted[i] == 'Destination Host Unreachable.':
                destination_unreachable_count += 1

        if request_time_out_count >= 3:
            return 'Request timed out.', parsed_array, raw_output
        elif destination_unreachable_count >= 3:
            return 'Destination Host Unreachable.', parsed_array, raw_output
        else:
            sent = int(parsed_result[0])
            received = int(parsed_result[1])
            loss = parsed_result[2]

            if sent == 4 and received == 4:
                return "Success.", parsed_array, raw_output
            elif received == 3:
                while count > 0:
                    perform_ping(host)
            else:
                return "Fail.", parsed_array, raw_output

    else:
        if 'Ping request could not find host' in parsed_array[0]:
            return 'Invalid IP/EP.', parsed_array, raw_output


