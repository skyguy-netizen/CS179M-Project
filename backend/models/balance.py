import copy
import utils.manifest_handler


def find_distance(grid, start, end):

    current_states = []
    past_states = set()
    hx = abs(start[0] - end[0]) + abs(start[1] - end[1])
    current_states.append([hx, 0, start[0], start[1]])


    past_states.add(str(start[0]) + str(start[1]))
    while True:
        if len(current_states) == 0:
            return -1
        curr = current_states.pop(0)

        
        if curr[2] == end[0] and curr[3] == end[1]:
            return curr[1]

        #up
        if curr[2]+1 < 10 and grid.grid[curr[2]+1][curr[3]] == 0:
            hx = abs(curr[2]+1 - end[0]) + abs(curr[3] - end[1])
            gx = curr[1]+1
            fx = hx+gx
            if not str(curr[2]+1) + str(curr[3]) in past_states:
                current_states.append([fx, gx, curr[2]+ 1, curr[3]])
                past_states.add(str(curr[2]+1) + str(curr[3]))
        #down
        
        if curr[2]-1 >= 0 and grid.grid[curr[2]-1][curr[3]] == 0:
            hx = abs(curr[2]-1 - end[0]) + abs(curr[3] - end[1])
            gx = curr[1]+1
            fx = hx+gx
            if not str(curr[2]-1) + str(curr[3]) in past_states:
                current_states.append([fx, gx, curr[2]- 1, curr[3]])
                past_states.add(str(curr[2]-1) + str(curr[3]))
        #left
        if curr[3]-1 >= 0 and grid.grid[curr[2]][curr[3]-1] == 0:
            hx = abs(curr[2] - end[0]) + abs(curr[3]-1 - end[1])
            gx = curr[1]+1
            fx = hx+gx
            if not str(curr[2]) + str(curr[3]-1 ) in past_states:
                current_states.append([fx, gx, curr[2], curr[3]-1])
                past_states.add(str(curr[2]) + str(curr[3]-1 ))
        #down
        if curr[3]+1 < 12 and grid.grid[curr[2]][curr[3]+1] == 0:
            hx = abs(curr[2] - end[0]) + abs(curr[3]+1 - end[1])
            gx = curr[1]+1
            fx = hx+gx
            if not str(curr[2]) + str(curr[3] +1) in past_states:
                current_states.append([fx, gx, curr[2], curr[3]+1])
                past_states.add(str(curr[2]) + str(curr[3] +1))

        current_states= sorted(current_states, key=lambda x: x[0])


class Grid:
    def __init__(self, fx= 0, grid=None, hx=0,gx=0, goal_state = False, lower_bound = 0, upper_bound = 0, id = 0, compression="", sift=False, moves = []):
        if grid is None:
            grid = [[None for i in range(12)] for i in range(10)] #[y][x] 
        self.grid = grid
        self.fx = fx
        self.gx = gx
        self.hx = hx
        self.goal_state = goal_state
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.id = id
        self.compression = compression
        self.sift = sift
        self.moves = moves

    def set_id(self, id):
        self.id = id
    
    def print_grid(self):
        for row in reversed(self.grid):
            for element in row:
                if element == -1:
                    print("N ",end="")
                else:
                    print(str(element) + " ",end="")
            print()
            
    def compress(self):
        compression = ""
        counter = 0
        curr_val = int(self.grid[0][0])
        for y in range(0,8):
            for x in range(0,12):
                if int(self.grid[y][x]) == curr_val:
                    counter+=1
                else:
                    compression+="("+str(counter)+")"+str(curr_val)
                    counter=1
                    curr_val = int(self.grid[y][x])
        self.compression=compression

    def calculate_hx(self):
        left_sum = 0
        right_sum = 0
        left_values = []
        right_values = []
        hx = 0
        for x in range(0,6):
            for y in range(0,8):
                if int(self.grid[y][x]) != -1:
                    left_sum += int(self.grid[y][x])
                if self.grid[y][x] != 0 and self.grid[y][x] != -1:
                    left_values.append(self.grid[y][x])
        for x in range(6,12):
            for y in range(0,8):
                if int(self.grid[y][x]) != -1:
                    right_sum += self.grid[y][x]  
                if self.grid[y][x] != 0 and self.grid[y][x] != -1:
                    right_values.append(self.grid[y][x])

        
        lower_bound = (left_sum+right_sum)/2.1
        upper_bound = (left_sum+right_sum)/1.9

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound


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



            
        
#initial state grid from file input
file_name = utils.manifest_handler.get_name()
f = open(file_name, "r+")
lines = f.readlines() 

initial_state = Grid()
for y in range(0,8):
    for x in range(0,12):
        if lines[12*y+x][18:] == "NAN\n":
            initial_state.grid[y][x] = -1
        elif int(lines[12*y+x][10:15]) > 0:
            initial_state.grid[y][x] = int(lines[12*y+x][10:15])
        else:
            initial_state.grid[y][x] = 0
for y in range(8,10):
    for x in range(0,12):
        initial_state.grid[y][x] = 0



initial_state.calculate_hx()



grids_states = []
past_states = set()

grids_states.append((initial_state.fx,initial_state))
initial_state.compress()
past_states.add(initial_state.compression)


if not initial_state.sift:

    id = 1
    i = 1
    while True:

        i+=1
        if len(grids_states) == 0:
            print("Unsolveable")
            break
        current_grid = grids_states[0][1]
        del grids_states[0]

        if current_grid.goal_state: 

            for move in current_grid.moves:
                print("Move container from " + str(move[0]) + " to " + str(move[1]))

            break

        empty_spaces = []
        for x in range(0,12):
            for y in range(0,8):
                if current_grid.grid[y][x] == 0: 
                    empty_spaces.append([y,x])
                    break


        container_location = []
        for x in range(0,12):
            for y in range(0,8):
                if current_grid.grid[y][x] != 0 and current_grid.grid[y][x] != -1 :
                    container_location.append([y,x])
                elif current_grid.grid[y][x] == 0:
                    break


        counter = 0


        for container_y, container_x in container_location:

            if current_grid.grid[container_y+1][container_x] != 0:
                continue
            for space_y, space_x in empty_spaces:
                if space_x == container_x:
                    continue
                new_grid = copy.deepcopy(current_grid)
                new_grid.moves.append([[container_y,container_x],[space_y,space_x]])
                new_grid.grid[space_y][space_x] = current_grid.grid[container_y][container_x]
                new_grid.grid[container_y][container_x] = 0

                

                new_grid.gx += find_distance(current_grid, [container_y, container_x],[space_y, space_x])
                new_grid.set_id(id)
                id+=1
                new_grid.calculate_hx()
                new_grid.compress()

                if not new_grid.compression in past_states:
                    grids_states.append((new_grid.fx,new_grid))

                    past_states.add(new_grid.compression)



        
        grids_states= sorted(grids_states, key=lambda x: x[0])

        
else:

    containers = []
    for x in range(0,12):
        for y in range(0,8):
            if initial_state.grid[y][x] != 0 and initial_state.grid[y][x] != -1 :
                # containers[initial_state.grid[y][x]] = [y,x]
                containers.append([initial_state.grid[y][x], [y,x]])
            elif initial_state.grid[y][x] == 0:
                break


    sorted_weights = sorted(containers)  


    buffer = Grid()
    

    start_y = 0
    start_x = 11
    for container in sorted_weights:
        print("Move container at ship location " + str(container[1][0]) + "," + str(container[1][1]) + " to buffer " + str(start_y) + "," + str(start_x) )

        buffer.grid[start_y][start_x] = container[0] #put container in buffer

        initial_state.grid[container[1][0]][ container[1][1]] = 0 #zero out ship grid
        container[1][0] = start_y
        container[1][1] = start_x
        start_y+=1
        if start_y == 9:
            start_x-=1
            start_y = 0

    
    
    
    sift_y = 0
    sift_x = 5

    sorted_weights.sort(reverse=True)


    sift_increment = 1
    sift_shift = True
    for container in sorted_weights:
        print("Move container at buffer location " + str(container[1][0]) + "," + str(container[1][1]) + " to ship " + str(sift_y) + "," + str(sift_x) )
        initial_state.grid[sift_y][ sift_x] = container[0] #place container back on ship
        buffer.grid[container[1][0]][container[1][1]] = 0 #zero out buffer
        if sift_shift:
            sift_x += sift_increment
            sift_increment +=1
            sift_shift = False
        else:
            sift_x -= sift_increment
            sift_increment +=1
            sift_shift = True






