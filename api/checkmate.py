from flask import Flask, render_template, request, jsonify
from tools import ping, telnet, traceroute, nslookup

app = Flask(__name__, template_folder="../templates", static_folder="../static")

# Home Page
@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/run", methods=['POST'])
def all_tests():
    if request.method == 'POST':
        checks_to_run = request.form.getlist('checks')
        print(len(checks_to_run))
        for i in range(len(checks_to_run)):
            if checks_to_run[i] == 'ping':
                print('running ping')
            elif checks_to_run[i] == 'traceroute':
                print('running traceroute')
            elif checks_to_run[i] == 'nslookup':
                print('running nslookup')
            elif checks_to_run[i] == 'telnet':
                print('running telnet')

    return jsonify('Running Tests')

@app.route("/ping", methods=['POST'])
def ping_host():
    if request.method == 'POST':
        endpoint = request.form['endpoint']
        output = ping.perform_ping(endpoint)
        return render_template('index.html', output=output)

@app.route("/telnet", methods=['POST'])
def telnet_host():
    if request.method == 'POST':
        endpoint = request.form['endpoint']
        output = telnet.check_if_port_open(host=endpoint, port=22)
        return render_template('index.html', output=output)

@app.route("/traceroute", methods=['POST'])
def traceroute_host():
    if request.method == 'POST':
        endpoint = request.form['endpoint']
        output = traceroute.trace_route_of_instance(endpoint)
        return render_template('index.html', output=output)

@app.route("/nslookup", methods=['POST'])
def nslookup_host():
    if request.method == 'POST':
        endpoint = request.form['endpoint']
        output = nslookup.name_to_ip(endpoint)
        return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
