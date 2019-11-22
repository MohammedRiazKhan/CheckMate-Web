from flask import Flask, render_template, request, jsonify
from tools import ping, telnet, traceroute, nslookup, instance

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Home Page
@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/run", methods=['POST'])
def all_tests():
    if request.method == 'POST':

        checks_to_run = request.form.getlist('checks')
        endpoint = request.form['endpoint']
        port = request.form['port']
        port = int(port)
        print(port)

        if endpoint == '' and len(checks_to_run) == 0:
            return render_template('index.html', endpoint_message="Please enter an IP or Endpoint",
                                   checkbox_message="Please select at least one test to run")
        if endpoint == '':
            return render_template('index.html', endpoint_message="Please enter an IP or Endpoint")
        if not instance.valid_ip(endpoint):
            return render_template('index.html', endpoint_message="Please enter a valid IP")
        if instance.is_public_ip(endpoint):
            return render_template('index.html', endpoint_message="Please enter a valid public IP")
        if len(checks_to_run) == 0:
            return render_template('index.html', checkbox_message="Please select at least one test to run")

        ping_out = []
        trace_out = []
        tel_out = []
        ns_out = []

        for i in range(len(checks_to_run)):
            if checks_to_run[i] == 'ping':
                ping_out = ping.perform_ping(endpoint)
            elif checks_to_run[i] == 'traceroute':
                trace_out = traceroute.trace_route_of_instance(endpoint)
            elif checks_to_run[i] == 'nslookup':
                ns_out = nslookup.name_to_ip(endpoint)
            elif checks_to_run[i] == 'telnet':
                tel_out = telnet.check_if_port_open(host=endpoint, port=port)

    print(tel_out)
    return render_template('index.html', ping_output=ping_out, telnet_output=tel_out, traceroute_output=trace_out, nslookup_output=ns_out)

@app.route("/ping", methods=['POST'])
def ping_host():
    if request.method == 'POST':
        endpoint = request.form['endpoint']
        output = ping.perform_ping(endpoint)
        return render_template('index.html', ping_output=output)

@app.route("/telnet", methods=['POST'])
def telnet_host():
    if request.method == 'POST':
        endpoint = request.form['endpoint']
        output = telnet.check_if_port_open(host=endpoint, port=22)
        return render_template('index.html', telnet_output=output)

@app.route("/traceroute", methods=['POST'])
def traceroute_host():
    if request.method == 'POST':
        endpoint = request.form['endpoint']
        output = traceroute.trace_route_of_instance(endpoint)
        return render_template('index.html', traceroute_output=output)

@app.route("/nslookup", methods=['POST'])
def nslookup_host():
    if request.method == 'POST':
        endpoint = request.form['endpoint']
        output = nslookup.name_to_ip(endpoint)
        return render_template('index.html', nslookup_output=output)

if __name__ == '__main__':
    app.run(debug=True)
