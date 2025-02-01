from flask import Flask, request
import numpy as np

app = Flask(__name__)
def test(n1, n2):
    return str(n1 + n2)

@app.route('/', methods=['GET'])
def hello_world():
    p1 = request.args.get('p1', '1')
    p2 = request.args.get('p2', '2')
    return f"{int(p1)+int(p2)}"

@app.route('/data', methods=['POST'])
def receive_data():
    data = "Hello"
    return data


if __name__ == '__main__':
    app.run(debug=True)
