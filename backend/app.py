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
from backend.models.init_balance import create_ship
from backend.models.user import set_user, get_user
from backend.utils.manifest_handler import set_file, set_name, get_file, get_name
from utils.log_handler import set_comment, get_comment
from backend.models.cargo import Cargo

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

ship = None
process = None
moves = None
LOG_FILE = None
manifest_name = None

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
        set_comment(comment)
        return{"Success":200}
    return {'comment': get_comment()}

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
        output_manifest = manifest_name.rsplit('.', 1)[0] + "OUTBOUND.txt"
        tm.update_manifest(output_manifest)
        moves = tm.get_paths()
        path = []
        ids = []
        times = []
        for move in moves:
            ids.append(move[0])
            path.append(move[1])
            times.append(move[2])
        return{'paths': path, 'ids': ids, 'times': times}

# @app.route("/log", methods=["GET"])
# @cross_origin()
# def log():
#     curr_year = datetime.datetime.now().year
#     file_name = str(curr_year) + "_log_file.log"
#     return send_from_directory(app.static_folder, file_name)
    
@app.route("/manifest", methods=["GET"])
@cross_origin(exposedHeaders = {"Content-Disposition"})
def manifest():
    file_name = get_name()
    output_filename = file_name[:-4] + "OUTBOUND.txt"
    static_folder_path = os.path.join(app.root_path, "static", "manifest")
    
    try:
        response = send_from_directory(static_folder_path, output_filename, mimetype='text/plain', as_attachment=True, download_name=f'{output_filename}')
        response.headers["Content-Disposition"] = f"attachment; filename={output_filename}"
        return response
    except Exception as e:
        print(f"Error occurred while sending file: {e}")
        return "File not found or error occurred", 404

def init_log_file():
    curr_year = datetime.datetime.now().year

    log_file = None
    suffix = "_log_file.log"

    for file in os.listdir('.'):
        if suffix in file:
            log_file = file
    
    if log_file:
        log_file_year = int(log_file.split('_')[0])
        if log_file_year != curr_year:
            os.remove(log_file)
            log_file = None
        
    if not log_file:
        log_file = f"{curr_year}{suffix}"

        open(log_file, 'w').close()

    global LOG_FILE
    LOG_FILE = log_file

if __name__ == '__main__':
    init_log_file()
    app.run(debug=True)