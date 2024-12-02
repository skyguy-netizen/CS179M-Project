class Ship:
    def __init__(self, shipgrid):
        # This grid will be 12 x 8 or whatever is the ship size
        # Each entry will be of object Cargo
        self.shipgrid = shipgrid

    def get_container_pos_by_name(self, container_name: str) -> tuple[int, int]:
        # Search from top to bottom, to get the topmost container
        for i in range(11, -1, -1): # Will loop from 11 to 0
            for j in range(8, -1, -1):
                if self.shipgrid[i][j].get_name() == container_name:
                    return (i, j)
                
        return (-1, -1) # Not found in the ship

    #def set_initial_heuristics(self, goal, containers):

    def can_move_container(self,location):
        x,y = location #row and column set to location passed in
        #check if row above container to be unloaded is open or not
        if x == len(self.shipgrid) - 1:
            return True
        else:
            return not self.shipgrid[len(self.shipgrid + 1)][len(self.shipgrid[0])]

    def find_shortest_column (self, col):
        for row in range (len(self.shipgrid) - 1):
            if not self.shipgrid[row][col]:
                return (row,col)
    
    def move_container (self, start, end):
        cargo = self.shipgrid[start[0]][start[1]]
        self.shipgrid[start[0]][start[1]] = None
        self.shipgrid[end[0]][end[1]] = cargo
        cargo.pos = end

    def top_most_container (self, col):
        for row in range (len(self.shipgrid)):
            if self.shipgrid[row][col]:
                return (row,col)
