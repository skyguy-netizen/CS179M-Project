from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from copy import deepcopy
import datetime
import sys, os
from io import BytesIO
import textwrap
from fpdf import FPDF


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.models.transfermanager import TransferManager
from backend.models.balance import Balance
from backend.models.user import set_user, get_user
from backend.utils.manifest_handler import set_file, set_name, get_file, get_name, create_ship
from utils.log_handler import set_comment, get_comment
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
manifest_name = None
file_name = None
balance_instance = None

@app.route("/fileUploadLoad", methods=["POST", "GET"])
@cross_origin()
def fileUploadLoad():
    if (request.method == 'POST'):
        if 'file' not in request.files:
            return "File not found!", 400
        file = request.files['file']
        global ship
        global manifest_name
        ship = set_file(file)
        manifest_name = file.filename

        with open(LOG_FILE, 'a') as log:
            msg = get_curr_time() + f"Manifest {file.filename} is loaded. There are {ship.get_containers()} containers on the ship\n"
            log.write(msg)
        
        print("Returning what")
        set_name(file.filename)
        return{"Success":200}
    print(get_file())
    return {'message': get_file()}

@app.route("/fileUploadBalance", methods=["POST", "GET"])
@cross_origin()
def fileUploadBalance():
    if (request.method == 'POST'):
        if 'file' not in request.files:
            return "File not found!", 400
        file = request.files['file']
        global ship
        global file_name
        file_name = file.filename
        set_name(file_name)
        # file_copy = deepcopy(file)

        ship = create_ship(file)
        with open(LOG_FILE, 'a') as log:
            msg = get_curr_time() + f"Manifest {file.filename} is loaded. There are {ship.get_containers()} containers on the ship\n"
            log.write(msg)
        # file_data = create_file_object(file_copy)
        return{"Success": 200}
    print(get_file())
    return {"message" : get_file()}

@app.route("/checkbalance", methods=["GET"])
@cross_origin()
def check_balance():
    global balance_instance
    balance_instance = Balance(ship, file_name, LOG_FILE)
    print(balance_instance.check_balance())
    return {"balance" : balance_instance.check_balance()}
    
@app.route("/balance", methods=["POST"])
@cross_origin()
def get_balance_info():
    
    balance_instance.balance()
    process = balance_instance.process
    path = []
    ids = []
    times = []
    print(process)
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

@app.route("/get_fileName", methods=["GET", "POST"])
@cross_origin()
def get_fileName():
    filename = get_name()
    output_filename = filename[:-4] + "OUTBOUND.txt"
    return {'file_name': output_filename}

@app.route("/comment", methods=["POST", "GET"])
@cross_origin()
def comment():
    if (request.method == 'POST'):
        comment = request.get_json()
        if not comment:
            return (jsonify({"Message": "You must include a comment"}), 400)
        print(comment)
        with open(LOG_FILE, 'a') as log:
            msg = get_curr_time() + comment['comment'] + '\n'
            log.write(msg)
        return{"Success":200}
    return {'comment': "No comment"}

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
        load_list = [Cargo(container_name=item[0], weight = item[1]) for item in load]
        unload_list = []
        print(ship_grid)
        for coord in unload:
            x, y = map(int, coord.strip("[]").split(","))
            print(x, y)
            unload_list.append(ship_grid[x - 1][ y - 1])
        print("Unload list: ", unload_list)
        unload_list_names = deepcopy(unload_list)
        tm = TransferManager(load_list,unload_list,ship, LOG_FILE)
        tm.set_goal_locations()
        tm.transfer_algorithm()
        output_manifest = manifest_name.rsplit('.', 1)[0] + "OUTBOUND.txt"
        tm.update_manifest(output_manifest)
        moves = tm.get_paths()
        path = []
        ids = []
        times = []
        ops_order = []
        load_names = [i[0] for i in load]
        unload_names = [c.get_name() for c in unload_list_names]
        print("Load: ", load_names)
        print("Unload: ", unload_names)
        for move in moves:
            ids.append(move[0])
            path.append(move[1])
            times.append(move[2])
            if move[0] in load_names:
                ops_order.append("L")
            elif move[0] in unload_names:
                ops_order.append("UL")
            else:
                pass
        print(ops_order)

        tm.clear_paths()
        with open(LOG_FILE, 'a') as log:
            msg = get_curr_time() + f"Finished a cycle. Manifest {output_manifest} was written to desktop, and a reminder pop-up to operator to send file was displayed\n"
            log.write(msg)
            
        return{'paths': path, 'ids': ids, 'times': times, 'opsOrder': ops_order}
    
@app.route("/manifest", methods=["GET"])
@cross_origin()
def manifest():
    file_name = get_name()
    output_filename = file_name[:-4] + "OUTBOUND.txt"
    static_folder_path = "../static/manifest"
    
    try:
        return send_from_directory(static_folder_path, output_filename, mimetype='text/plain', as_attachment=True)
    except Exception as e:
        print(f"Error occurred while sending file: {e}")
        return "File not found or error occurred", 404

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