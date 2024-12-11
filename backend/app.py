from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from copy import deepcopy
import datetime

import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.models.transfermanager import TransferManager
from backend.models.balance import Balance
from backend.models.init_balance import create_ship
from backend.models.user import set_user, get_user
from backend.utils.manifest_handler import set_file, set_name, get_file
from backend.models.cargo import Cargo
from backend.utils.functions_util import get_curr_time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ship = None
process = None
moves = None
user = None
LOG_FILE = None

@app.route("/fileUploadLoad", methods=["POST", "GET"])
@cross_origin()
def fileUploadLoad():
    if (request.method == 'POST'):
        if 'file' not in request.files:
            return "File not found!", 400
        file = request.files['file']
        global ship
        ship = set_file(file)

        with open(LOG_FILE, 'a') as log:
            msg = get_curr_time() + f"Manifest {file.filename} is loaded. There are {ship.get_containers()} containers on the ship\n"
            log.write(msg)
        

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
        balance_instance = Balance(ship, file_name, LOG_FILE)
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
        
        global user
        prev_user = deepcopy(user)
        user = first_name['first_name']

        with open(LOG_FILE, 'a') as log:
            time = get_curr_time()
            msg = ""
            if prev_user:
                msg += f"{time}{prev_user} signs out\n"
                
            msg += f"{time}{user} signs in\n"
            log.write(msg)
        return{"Success":200}
    return {'first_name': get_user()}

@app.route("/load", methods=["POST", "GET"])
@cross_origin()
def get_transfer_info():
    print("test")
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
        tm = TransferManager(load_list,unload_list,ship, LOG_FILE)
        tm.set_goal_locations()
        tm.transfer_algorithm()
        tm.update_manifest()
        moves = tm.get_paths()
        path = []
        ids = []
        times = []
        for move in moves:
            ids.append(move[0])
            path.append(move[1])
            times.append(move[2])

        with open(LOG_FILE, 'a') as log:
            msg = get_curr_time() + "Finished a cycle. Manifest {manifest_outbound_name} was written to desktop, and a reminder pop-up to operator to send file was displayed\n"
            log.write(msg)
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

def init_log_file():
    curr_year = datetime.datetime.now().year

    log_file = None
    prefix = "KeoghsPort"

    for file in os.listdir('.'):
        if prefix in file:
            log_file = file
    
    if log_file:
        log_file_year = int(log_file.split('.')[0][-4:])
        if log_file_year != curr_year:
            os.remove(log_file)
            log_file = None
        
    if not log_file:
        log_file = f"{prefix}{curr_year}.txt"

        open(log_file, 'w').close()

    global LOG_FILE
    LOG_FILE = log_file

if __name__ == '__main__':
    init_log_file()
    app.run(debug=True)