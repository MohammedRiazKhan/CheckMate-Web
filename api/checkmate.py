from flask import Flask
from flask import jsonify
from tools import instance_ping as ping

app = Flask(__name__)

ip = '127.0.0.1'

@app.route("/", methods=['GET', 'POST'])
def hello():

    ping_output = ping.test_ping(ip)

    return jsonify({'ping_result': ping_output})

@app.route("/ping/{ip}", methods=['POST'])
def perform_ping():
    return ""

if __name__ == '__main__':
    app.run(debug=True)
