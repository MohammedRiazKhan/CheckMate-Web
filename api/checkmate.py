from flask import Flask, render_template, request, jsonify
from tools import ping, telnet, traceroute, nslookup

app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")

# Home Page
@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/ping", methods=['POST'])
def ping_host():
    if request.method == 'POST':
        endpoint = request.form['host']
        output = ping.perform_ping(endpoint)
        return render_template('index.html', output=output)

@app.route("/telnet", methods=['POST'])
def telnet_host():
    if request.method == 'POST':
        endpoint = request.form['host']
        output = telnet.check_if_port_open(host=endpoint, port=22)
        return render_template('index.html', output=output)

@app.route("/traceroute", methods=['POST'])
def traceroute_host():
    if request.method == 'POST':
        endpoint = request.form['host']
        output = traceroute.trace_route_of_instance(endpoint)
        return render_template('index.html', output=output)

@app.route("/nslookup", methods=['POST'])
def nslookup_host():
    if request.method == 'POST':
        endpoint = request.form['host']
        output = nslookup.name_to_ip(endpoint)
        return render_template('index.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)
