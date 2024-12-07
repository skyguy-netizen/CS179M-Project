from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from models.user import set_user, get_user
from utils.manifest_handler import set_file, set_name, get_file
from models.transfermanager import TransferManager
from models.balance import Balance
from models.init_balance import create_ship
from copy import deepcopy
from models.cargo import Cargo

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ship = None
process = None
moves = None

@app.route("/fileUploadLoad", methods=["POST", "GET"])
@cross_origin()
def fileUploadLoad():
    if (request.method == 'POST'):
        if 'file' not in request.files:
            return "File not found!", 400
        file = request.files['file']
        global ship
        ship = set_file(file)
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
        file_name = file.filename
        ship = create_ship(file)
        balance_instance = Balance(ship, file_name)
        balance_instance.balance()
        process = balance_instance.process
        return{"Success": 200}
    path = []
    ids = []
    times = []
    for move in process:
        ids.append(move[0])
        times.append(move[1])
        path.append(move[2])
    return {'paths': path, 'ids': ids, 'times': times}

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

@app.route("/load", methods=["POST", "GET"])
@cross_origin()
def get_transfer_info():
    if(request.method == "POST"):
        data = request.get_json()
        load = data.get('load')
        unload = data.get('unload')
        print(load)
        print(unload)
        ship_grid = [[None for _ in range(12)] for _ in range(8)]
        ship_grid = ship.shipgrid
        load_list = [Cargo(name, None) for name in load]
        unload_list = []
        print(ship_grid)
        for coord in unload:
            x, y = map(int, coord.strip("[]").split(","))
            unload_list.append(ship_grid[x - 1][ y - 1])
        print(unload_list)
        tm = TransferManager(load_list,unload_list,ship)
        tm.set_goal_locations()
        tm.transfer_algorithm()
        moves = tm.get_paths()
        return{"Success":200}
    path = []
    ids = []
    times = []
    for move in moves:
        ids.append(move[0])
        path.append(move[1])
        times.append(move[2])
    return{'paths': path, 'ids': ids, 'times': times}
    
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