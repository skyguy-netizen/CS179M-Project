import pandas as pd
from flask import jsonify
from backend.models.cargo import Cargo
from backend.models.ship import Ship
from copy import deepcopy

file = None

def convert_position(curr_index):
    x = curr_index//12
    y = curr_index%12
    return (x,y)

def create_file_object(file_):
    df = pd.read_csv(file_, header=None, delimiter = ', ', engine='python')
    matrix = df.to_numpy()
    matrix = matrix.tolist()
    return (matrix, matrix, file_)


def create_ship(file_):
    
    # f = deepcopy(file_)
    f = file_
    lines = f.readlines()
    f.seek(0)

    global file
    (file, _, f) = create_file_object(f)

    
    
    
   
    initial_state = [[None for i in range(12)] for i in range(10)]

    for y in range(0,8):
        for x in range(0,12):
            if lines[12*y+x][18:].decode('utf-8').strip() == "NAN":
                initial_state[y][x] = -1
            elif int(lines[12*y+x][10:15]) > 0:
                name = lines[12*y+x][18:].decode('utf-8').strip()
                weight = int(lines[12*y+x][10:15].decode('utf-8'))
                temp = Cargo(name, (x,y), weight)
                initial_state[y][x] = temp
            else:
                initial_state[y][x] = 0

    for y in range(8,10):
        for x in range(0,12):
            initial_state[y][x] = 0

    ship_object = Ship(initial_state)
    return ship_object

def set_file(file_):
    global file 
    
    list = []
    (file, matrix, _) = create_file_object(file_)

    shipgrid = [[None] * 12 for i in range(8)]
    
    
    for i, data in enumerate(matrix):
        x,y = convert_position(i)
        # position = i[0]
        weight = data[1]
        weight_str = weight.split("{")[1].split("}")[0]
        # print(weight_str)
        int_weight = int(weight_str)
        container_name = data[2]
        # print(type(container_name))
        if container_name.upper() == "UNUSED":
            # print("Found unused at ", (x,y))
            continue
        elif container_name.upper() == "NAN":
            # print("Found NAN at ", (x,y))
            obj = Cargo("Blocked", (x,y))
        else:
            obj = Cargo(container_name, (x,y))
        list.append(obj)
        obj.set_weight(int_weight)
        shipgrid[x][y] = deepcopy(obj)
    
    ship = Ship(shipgrid)
    return ship

file_name = ""
        
def set_name(name):
    global file_name
    file_name = name

def get_file():
    global file
    return file

def get_name():
    global file_name
    return file_name