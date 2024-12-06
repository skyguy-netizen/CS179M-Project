from backend.models.cargo import Cargo
from backend.utils.functions_util import get_path
from typing import List

class Ship:
    OPEN_POS = (8, 0)
    def __init__(self, shipgrid: List[List[Cargo]]):
        # This grid will be 8 x 12 or whatever is the ship size
        # Each entry will be of object Cargo
        self.shipgrid = shipgrid
        self.rows = len(shipgrid)
        self.cols = len(shipgrid[0])
    
    def __repr__(self):
        cell_width = 10
        fin_str = ""
        for row in self.shipgrid:
            fin_str += " | ".join(
                    f"{str(cell):^{cell_width}}" if cell is not None else f"{'None':^{cell_width}}"
                    for cell in row
                )
            fin_str += "\n"
        return fin_str

    def get_container_pos_by_name(self, container_name: str) -> tuple[int, int]:
        # Search from top to bottom, to get the topmost container
        for i in range(11, -1, -1): # Will loop from 11 to 0
            for j in range(8, -1, -1):
                if self.shipgrid[i][j].get_name() == container_name:
                    return (i, j)
                
        return (-1, -1) # Not found in the ship

    def can_move_container(self,location):
        x,y = location #row and column set to location passed in
        #check if row above container to be unloaded is open or not
        if x == len(self.shipgrid) - 1:
            return True
        else:
            print("Location to check", location)
            return not self.shipgrid[x + 1][y]

    def find_shortest_column(self, col):
        # This will go from bottom to top in that column and will return the lowest open positions
        for row in range(self.rows):
            if not self.shipgrid[row][col]:
                return (row,col)
        return (None, None)
    
    def manhattan_distance_calculation(self,start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def move_container(self, old_pos, new_pos):
        cargo = self.shipgrid[old_pos[0]][old_pos[1]]

        path_trace = get_path(old_pos, new_pos)
        move_cost = self.manhattan_distance_calculation(old_pos, new_pos) + 2
        name = cargo.get_name()

        self.shipgrid[old_pos[0]][old_pos[1]] = None
        if new_pos != self.OPEN_POS:
            self.shipgrid[new_pos[0]][new_pos[1]] = cargo
        cargo.set_pos(new_pos)  # Update cargo's position

        return (name, path_trace, move_cost)

    def top_most_container(self, col):
        # This will go top to bottom and find the highest occupied spot
        # print(self.shipgrid)
        for row in range(self.rows - 1, -1, -1):        
            if self.shipgrid[row][col]:
                return (row,col)
