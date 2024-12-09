import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.ship import Ship
from models.cargo import Cargo
from models.buffer import Buffer
from models.balance import Balance

def create_ship(file):
    f = file
    lines = f.readlines() 

    initial_state = [[None for i in range(12)] for i in range(10)]

    for y in range(0,8):
        for x in range(0,12):
            if lines[12*y+x][18:] == "NAN\n":
                initial_state[y][x] = -1
            elif int(lines[12*y+x][10:15]) > 0:
                temp = Cargo(lines[12*y+x][18:], (x,y))
                temp.weight = int(lines[12*y+x][10:15])
                initial_state[y][x] = temp

            else:
                initial_state[y][x] = 0
    for y in range(8,10):
        for x in range(0,12):
            initial_state[y][x] = 0

    return Ship(initial_state)

