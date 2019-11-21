from flask import Flask
from flask import jsonify
from tools import ping
from tools import nslookup
from tools import telnet
from tools import traceroute
from flask import render_template

app = Flask(__name__, template_folder="../web/templates")

@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
