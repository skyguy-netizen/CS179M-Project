from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from utils import manifest_handler
from models import user

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/fileUpload", methods=["POST", "GET"])
@cross_origin()
def fileUpload():
    if (request.method == 'POST'):
        if 'file' not in request.files:
            return "File not found!", 400
        file = request.files['file']
        manifest_handler.set_file(file)
        manifest_handler.set_name(file.filename)
        return("Success")
    return {'message': manifest_handler.get_file()}

@app.route("/login", methods=["POST", "GET"])
@cross_origin()
def login():
    if (request.method == 'POST'):
        first_name = request.get_json()
        if not first_name:
            return (jsonify({"Message": "You must include a first name."}), 400)
        user.set_user(first_name)
        return("Success")
    return {'first_name': user.get_user()}
    
if __name__ == '__main__':
    app.run(debug=True)