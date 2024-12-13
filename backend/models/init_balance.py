import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.ship import Ship
from models.cargo import Cargo
from models.buffer import Buffer
from models.balance import Balance

def create_ship(file):
    f = file
    lines = f.readlines()
    # print(lines)
    initial_state = [[None for i in range(12)] for i in range(10)]

    for y in range(0,8):
        for x in range(0,12):
            if lines[12*y+x][18:] == "NAN\n":
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

