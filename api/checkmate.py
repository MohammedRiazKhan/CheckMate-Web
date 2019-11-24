from flask import Flask, render_template, request, jsonify
from tools import ping, telnet, traceroute, nslookup, instance

app = Flask(__name__, template_folder="../templates", static_folder="../static")


# Home Page
@app.route("/")
def home():
    return render_template('index.html')


@app.route("/run", methods=['POST'])
def all_tests():
    if request.method == 'POST':

        instance_type = ''
        endpoint = request.form['endpoint']
        print(endpoint)
        checks_to_run = request.form.getlist('checks')
        print(checks_to_run)
        port = request.form['port']
        print(port)

        if endpoint == '' and len(checks_to_run) == 0 and port == '0':
            return render_template('index.html', endpoint_message="Please enter an IP or Endpoint",
                                   checkbox_message="Please select at least one test to run",
                                   dropdown_message="Please select a port to test")

        if endpoint == '':
            return render_template('index.html', endpoint_message="Please enter an IP or Endpoint")
        if len(checks_to_run) == 0:
            return render_template('index.html', checkbox_message="Please select at least one test to run")

        if len(checks_to_run) >= 1 and 'telnet' in checks_to_run and port == '0':
            return render_template('index.html', checkbox_message="Please select a port to test with telnet")

        if instance.determine_if_ip_or_endpoint(endpoint) == 'IP':
            instance_type = instance.determine_instance_type_by_ip(endpoint)

        elif instance.determine_if_ip_or_endpoint(endpoint) == 'Endpoint':
            instance_type = instance.determine_instance_type_by_endpoint(endpoint)

        elif instance.determine_if_ip_or_endpoint(endpoint) == 'Private IP':
            return render_template('index.html', endpoint_message="Please enter a valid public IP")

        elif instance.determine_if_ip_or_endpoint(endpoint) == 'Invalid IP':
            return render_template('index.html', endpoint_message="Please enter a valid IP or endpoint")

        ping_out = []
        trace_out = []
        tel_out = []
        ns_out = []

        if instance_type == 'Not a valid AWS resource':
            return render_template('index.html', endpoint_message="Not a valid AWS resource")

        elif instance_type == 'EC2':
            for i in range(len(checks_to_run)):
                if checks_to_run[i] == 'ping':
                    ping_out = ping.perform_ping(endpoint)
                elif checks_to_run[i] == 'traceroute':
                    trace_out = traceroute.trace_route_of_instance(endpoint)
                elif checks_to_run[i] == 'nslookup':
                    ns_out = nslookup.name_to_ip(endpoint)
                elif checks_to_run[i] == 'telnet':
                    port = int(port)
                    tel_out = telnet.check_if_port_open(host=endpoint, port=port)
        elif instance_type == 'RDS':
            for i in range(len(checks_to_run)):
                if checks_to_run[i] == 'ping':
                    ping_out = ['ICMP Packets are blocked on RDS', ['ICMP Packets are blocked on RDS'], ['ICMP Packets are blocked on RDS']]
                elif checks_to_run[i] == 'traceroute':
                    trace_out = ['ICMP Packets are blocked on RDS', ['ICMP Packets are blocked on RDS'], ['ICMP Packets are blocked on RDS']]
                elif checks_to_run[i] == 'nslookup':
                    ns_out = nslookup.name_to_ip(endpoint)
                elif checks_to_run[i] == 'telnet':
                    port = int(port)
                    tel_out = telnet.check_if_port_open(host=endpoint, port=port)

    return render_template('results.html', ping_output=ping_out, telnet_output=tel_out,
                           traceroute_output=trace_out, nslookup_output=ns_out, port=port)


if __name__ == '__main__':
    app.run(debug=True)
