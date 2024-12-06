from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from models.user import set_user, get_user
from utils.manifest_handler import set_file, set_name, get_file

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/fileUploadLoad", methods=["POST", "GET"])
@cross_origin()
def fileUploadLoad():
    if (request.method == 'POST'):
        if 'file' not in request.files:
            return "File not found!", 400
        file = request.files['file']
        set_file(file)
        set_name(file.filename)
        return{"Success":200}
    return {'message': get_file()}

@app.route("/fileUploadBalance", methods=["POST", "GET"])
@cross_origin()
def fileUploadBalance():
    if (request.method == 'POST'):
        if 'file' not in request.files:
            return "File not found!", 400
        file = request.files['file']
        set_file(file)
        set_name(file.filename)
        balance
        return{"Success": 200}
    return {'message': get_file()}

@app.route("/login", methods=["POST", "GET"])
@cross_origin()
def login():
    if (request.method == 'POST'):
        first_name = request.get_json()
        if not first_name:
            return (jsonify({"Message": "You must include a first name."}), 400)
        set_user(first_name)
        return{"Success":200}
    return {'first_name': get_user()}

@app.route("/load", methods=["POST"])
@cross_origin()
def get_transfer_info():
    data = request.get_json()
    load = data.get('load')
    unload = data.get('unload')
    print(load)
    print(unload)
    return{'load': load, 'unload': unload}
    
# You will get a list of container ids to unload/load
# Use that and create the load and unload lists and run the algorithm, algorithm should have the steps in lists, which you can get using .get_unload_paths and .get_load_paths
# Also add container_id to the path lists, instead of name (or keep name it doesn't matter)
# this will probably have to be converted into a dictionary like:

# {
#   paths: [all the paths] -> list of lists
#   ids: should match the above indices -> list
#   times: should match the above indices -> list
# }    

@app.route("/balance", methods=["POST"])
@cross_origin()
def balance():
    
    return{'Success':200}

if __name__ == '__main__':
    app.run(debug=True)