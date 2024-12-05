from backend.models.cargo import Cargo
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
    
    def move_container(self, old_pos, new_pos):
        path_trace = []
        cargo = self.shipgrid[old_pos[0]][old_pos[1]]

        curr_pos = old_pos
        while curr_pos != new_pos:
            #check down
            if curr_pos[0] < new_pos[0]:
                curr_pos = (curr_pos[0] + 1, curr_pos[1])
            #check up
            elif curr_pos[0] > new_pos[0]:
                curr_pos = (curr_pos[0] - 1, curr_pos[1])
            #check right
            elif curr_pos[1] < new_pos[1]:
                curr_pos = (curr_pos[0], curr_pos[1] + 1)
            #check left
            elif curr_pos[1] > new_pos[1]:
                curr_pos = (curr_pos[0], curr_pos[1] - 1)

            path_trace.append(curr_pos)

        self.shipgrid[old_pos[0]][old_pos[1]] = None
        if new_pos != self.OPEN_POS:
            self.shipgrid[new_pos[0]][new_pos[1]] = cargo
        cargo.set_pos(new_pos)  # Update cargo's position

        return path_trace

    def top_most_container(self, col):
        # This will go top to bottom and find the highest occupied spot
        # print(self.shipgrid)
        for row in range(self.rows - 1, -1, -1):        
            if self.shipgrid[row][col]:
                return (row,col)

    # def find_neighbors(self,location):
    #     row,col = location
    #     neighbors = []
    #     if row > 0 and not self.shipgrid[row + 1][col]: #up
    #         neighbors.append((row - 1, col)) 
    #     if row < len(self.shipgrid) - 1 and not self.shipgrid[row - 1][col]: #down
    #         neighbors.append((row + 1, col))
    #     if col > 0 and not self.shipgrid[row][col - 1]: #left
    #         neighbors.append((row, col - 1))
    #     if col < len(self.shipgrid[0]) - 1 and not self.shipgrid[row][col + 1]: #right
    #         neighbors.append((row, col + 1))
    #     return neighbors