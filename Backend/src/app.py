from flask import Flask, jsonify, request
from flask_cors import CORS
from parser_ import *
from Commands.Execute import execute

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return '<h1>Flask is running!</h1>'

@app.route("/api")
def api():
    return jsonify({"message": "Hello, World!"})

@app.route("/api/command", methods=["POST"])
def command():
    data = request.get_json()
    print(data["command"])
    
    parser = get_parser()
    parse_result = parser.parse(data["command"])
    return jsonify(parse_result)


if __name__ == "__main__":
    app.run(debug=True)