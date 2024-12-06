from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from utils import manifest_handler
from models import transfermanager as TransferManager
from models import user
from copy import deepcopy
from models import cargo as Cargo

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

@app.route("/load", methods=["POST"])
@cross_origin()
def get_transfer_info():
    data = request.get_json()
    load = data.get('load')
    unload = data.get('unload')
    ship_grid = [[None for _ in range(12)] for _ in range(8)]
    ship = manifest_handler.set_file(data)
    ship_grid = ship.shipgrid
    load_list = [Cargo(name, None) for name in load]
    unload_list = [deepcopy(ship_grid[pos[0]][pos[1]]) for pos in unload]
    tm = TransferManager(load_list,unload_list,ship)
    tm.set_goal_locations()
    tm.transfer_algorithm()

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
if __name__ == '__main__':
    app.run(debug=True)