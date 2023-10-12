from flask import Flask, jsonify, request
from flask_cors import CORS
from parser_ import *
import os, base64, mimetypes

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return jsonify({"name": "Robin Omar Buezo Díaz", "carnet": "201944994"})

@app.route("/api")
def api():
    return jsonify({"message": "Hello, World!"})

@app.route("/api/command", methods=["POST"])
def command():
    data = request.get_json()
    # print(data["command"])
    data["command"] = data["command"].replace("\\", "/")
    commands = data["command"].split("\n")
    
    parser = get_parser()
    result = ""
    line = 1
    for command in commands:
        result += f"Linea {line}: {command}\n\n"
        line += 1
        if command == '' or command[0] == '#':
            continue
        try:
            result += parser.parse(command)
        except Exception as e:
            result += f"{e}\n"
            

    return jsonify({
        "status": "success",
        "result": result,
        "error": ""
    })

@app.route("/getPics", methods=["GET"])
def getPics():
    path = request.args.get('path')

    if path == None:
        path = os.getcwd()
    else:
        path = path.replace("\\", "/")

    print(path)

    try:
        files = os.listdir(path)

        image_files = [file for file in files if file.lower().endswith((".jpg", ".png", ".jpeg", ".gif"))]

        images_info = []
        for image_file in image_files:
            image_path = os.path.join(path, image_file)

            with open(image_path, "rb") as image:
                base64_data = base64.b64encode(image.read()).decode("utf-8")

            mime_type = mimetypes.guess_type(image_path)[0]
            if mime_type == None:
                mime_type = "application/octet-stream"

            image_info = {
                "name": image_file,
                "path": image_path,
                "base64": base64_data,
                "mime": mime_type
            }
            images_info.append(image_info)

        return jsonify({
            "status": "success",
            "result": images_info,
            "error": ""
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "result": "",
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)