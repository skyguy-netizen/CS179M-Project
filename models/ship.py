from models.cargo import Cargo
from typing import List

class Ship:
    OPEN_POS = (8, 0)
    def __init__(self, shipgrid: List[List[Cargo]], fx= 0,  hx=0,gx=0, goal_state = False, compression="", sift=False, moves = [], total_moves = []):
        # This grid will be 8 x 12 or whatever is the ship size
        # Each entry will be of object Cargo
        self.shipgrid = shipgrid
        self.rows = len(shipgrid)
        self.cols = len(shipgrid[0])
        self.fx = fx
        self.gx = gx
        self.hx = hx
        self.goal_state = goal_state
        self.compression = compression
        self.sift = sift
        self.moves = moves
        self.total_moves = total_moves
    
    def calculate_hx(self):
        left_sum = 0
        right_sum = 0
        left_values = []
        right_values = []
        hx = 0

        for x in range(0,6):
            for y in range(0,8):
                if isinstance(self.shipgrid[y][x], Cargo):
                    left_sum += self.shipgrid[y][x].weight
                    left_values.append(self.shipgrid[y][x].weight)
        for x in range(6,12):
            for y in range(0,8):
                if isinstance(self.shipgrid[y][x], Cargo):
                    right_sum += self.shipgrid[y][x].weight
                    right_values.append(self.shipgrid[y][x].weight)

        
        lower_bound = (left_sum+right_sum)/2.1
        upper_bound = (left_sum+right_sum)/1.9

        right_values.sort(reverse=True)
        left_values.sort(reverse=True)

        if right_sum > lower_bound and right_sum < upper_bound:
            self.goal_state = True
    

        if left_sum > right_sum:
            counter = 0
            while not (right_sum > lower_bound and right_sum < upper_bound):
                if counter == len(left_values):
                    self.sift = True
                    break
                else:
                    counter = 0
                for value in left_values:
                    if right_sum + value <= upper_bound:
                        left_values.remove(value)
                        right_values.append(value)
                        right_sum = sum(right_values)
                        hx+=1
                        break
                    else:
                        counter+=1
        else:
            counter = 0
            while not (left_sum > lower_bound and left_sum < upper_bound):
                if counter == len(right_values):
                    self.sift = True
                    break
                else:
                    counter = 0
                for value in right_values:
                    if left_sum + value <= upper_bound:
                        right_values.remove(value)
                        left_values.append(value)
                        left_sum = sum(left_values)
                        hx+=1
                        break
                    else:
                        counter+=1

        self.hx = hx
        self.fx = hx + self.gx

    def compress(self):
        compression = ""
        counter = 0
        curr_val = 0
        if isinstance(self.shipgrid[0][0], Cargo):
            curr_val = self.shipgrid[0][0].weight
        else:
            curr_val = int(self.shipgrid[0][0])
        for y in range(0,8):
            for x in range(0,12):
                if (isinstance(self.shipgrid[y][x], Cargo)):
                    if self.shipgrid[y][x].weight == curr_val:
                        counter+=1
                    else:
                        compression+="("+str(counter)+")"+str(curr_val)
                        counter=1
                        curr_val = self.shipgrid[y][x].weight
                else: 
                    if (int(self.shipgrid[y][x]) == curr_val):
                        counter+=1
                    else:
                        compression+="("+str(counter)+")"+str(curr_val)
                        counter=1
                        curr_val = int(self.shipgrid[y][x])
        self.compression=compression

    def find_distance(self,start, end):
        current_states = []
        past_states = set()
        hx = abs(start[0] - end[0]) + abs(start[1] - end[1])
        current_states.append([hx, 0, start[0], start[1], [[start[0], start[1]]]])


        past_states.add(str(start[0]) + str(start[1]))

        while True:
            if len(current_states) == 0:
                return -1
            curr = current_states.pop(0)

            
            if curr[2] == end[0] and curr[3] == end[1]:
                return curr[1], curr[4]

            #up
            if curr[2]+1 < 10 and self.shipgrid[curr[2]+1][curr[3]] == 0:
                hx = abs(curr[2]+1 - end[0]) + abs(curr[3] - end[1])
                gx = curr[1]+1
                fx = hx+gx
                if not str(curr[2]+1) + str(curr[3]) in past_states:

                    temp = curr[4][:]
                    temp.append([curr[2]+ 1, curr[3]])
                    
                    current_states.append([fx, gx, curr[2]+ 1, curr[3], temp])
                    past_states.add(str(curr[2]+1) + str(curr[3]))

            #down
            
            if curr[2]-1 >= 0 and self.shipgrid[curr[2]-1][curr[3]] == 0:
                hx = abs(curr[2]-1 - end[0]) + abs(curr[3] - end[1])
                gx = curr[1]+1
                fx = hx+gx
                if not str(curr[2]-1) + str(curr[3]) in past_states:
                    temp = curr[4][:]
                    temp.append([curr[2]- 1, curr[3]])

                    current_states.append([fx, gx, curr[2]- 1, curr[3], temp])
                    past_states.add(str(curr[2]-1) + str(curr[3]))
            #left
            if curr[3]-1 >= 0 and self.shipgrid[curr[2]][curr[3]-1] == 0:
                hx = abs(curr[2] - end[0]) + abs(curr[3]-1 - end[1])
                gx = curr[1]+1
                fx = hx+gx
                if not str(curr[2]) + str(curr[3]-1 ) in past_states:
                    temp = curr[4][:]
                    temp.append([curr[2], curr[3]-1])

                    current_states.append([fx, gx, curr[2], curr[3]-1, temp])
                    past_states.add(str(curr[2]) + str(curr[3]-1 ))
            #down
            if curr[3]+1 < 12 and self.shipgrid[curr[2]][curr[3]+1] == 0:
                hx = abs(curr[2] - end[0]) + abs(curr[3]+1 - end[1])
                gx = curr[1]+1
                fx = hx+gx
                if not str(curr[2]) + str(curr[3] +1) in past_states:
                    temp = curr[4][:]
                    temp.append([curr[2], curr[3]+1])
                    current_states.append([fx, gx, curr[2], curr[3]+1, temp])
                    past_states.add(str(curr[2]) + str(curr[3] +1))

            current_states= sorted(current_states, key=lambda x: x[0])

            
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
        cargo = self.shipgrid[old_pos[0]][old_pos[1]]
        self.shipgrid[old_pos[0]][old_pos[1]] = None
        if new_pos != self.OPEN_POS:
            self.shipgrid[new_pos[0]][new_pos[1]] = cargo
        cargo.set_pos(new_pos)  # Update cargo's position


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