import copy
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.models.ship import Ship
from backend.models.cargo import Cargo
from backend.models.buffer import Buffer

def print_grid(grid):
        for row in reversed(grid):
            for element in row:
                if element == -1:
                    print("N ",end="")
                elif isinstance(element,Cargo):
                    print(element.weight, end = " ")
                else:
                    print(str(element) + " ",end="")
            print()


class Balance:
    def __init__ (self, ship: Ship, input_file):
        self.initial = ship
        self.input_file = input_file
        self.moves = []
        self.sub_moves = []
        self.process = []
        if not log_file:
            raise Exception("Log file required!!")
        self.log_file = log_file

    
    def balance(self):
        self.initial.calculate_hx()
        print_grid(self.initial.shipgrid)
        if self.initial.goal_state:
            return
        if not self.initial.sift:
            self.balance_iter()
        else:
            self.sift()
        self.update_manifest()

    def balance_iter(self):
        grids_states = []
        past_states = set()


        containers = []
        for x in range(0,12):
            for y in range(0,8):
                if isinstance(self.initial.shipgrid[y][x], Cargo):
                    containers.append(self.initial.shipgrid[y][x])
                elif self.initial.shipgrid[y][x] == 0:
                    break

        grids_states.append((self.initial.fx, self.initial))
        self.initial.compress()
        past_states.add(self.initial.compression)

        while True:
            if len(grids_states) == 0:
                self.sift()
                break

            current_grid = grids_states[0][1]
            del grids_states[0]
            if current_grid.goal_state: 
                self.initial = copy.deepcopy(current_grid)

                self.moves = current_grid.moves
                self.sub_moves = current_grid.total_moves

                for i in range(len(self.moves)):
                    self.process.append([str(current_grid.names[i])[2:(len(current_grid.names[i]))], current_grid.distances[i], current_grid.total_moves[i]])

                break

            empty_spaces = []
            for x in range(0,12):
                for y in range(0,8):
                    if current_grid.shipgrid[y][x] == 0: 
                        empty_spaces.append([y,x])
                        break
            
            container_location = []
            for x in range(0,12):
                for y in range(0,8):
                    if isinstance(current_grid.shipgrid[y][x], Cargo) :
                        container_location.append([y,x])
                    elif current_grid.shipgrid[y][x] == 0:
                        break
            
            for container_y, container_x in container_location:
                if current_grid.shipgrid[container_y+1][container_x] != 0:
                    continue
                for space_y, space_x in empty_spaces:
                    if space_x == container_x:
                        continue

                    new_grid = copy.deepcopy(current_grid)
                    new_grid.shipgrid[space_y][space_x] = current_grid.shipgrid[container_y][container_x]
                    new_grid.shipgrid[container_y][container_x] = 0
                    
                    dist, moves = current_grid.find_distance([container_y, container_x],[space_y, space_x])
                    new_grid.total_moves.append(moves)
                    new_grid.moves.append([[container_y, container_x],[space_y, space_x]])
                    new_grid.names.append(current_grid.shipgrid[container_y][container_x].container_name)
                    new_grid.distances.append(dist)

                    new_grid.gx += dist

                    if len(new_grid.times) == 0:
                        new_grid.times.append(dist)
                    else:
                        new_grid.times.append(new_grid.times[len(new_grid.times)-1] + dist)
                    new_grid.calculate_hx()
                    new_grid.compress()

                    if not new_grid.compression in past_states:
                        grids_states.append((new_grid.fx,new_grid))

                        past_states.add(new_grid.compression)

            grids_states= sorted(grids_states, key=lambda x: x[0])
    
    
    def sift(self):
        containers = []
        for x in range(0,12):
            for y in range(0,8):
                if isinstance(self.initial.shipgrid[y][x], Cargo):
                    containers.append((self.initial.shipgrid[y][x].weight, self.initial.shipgrid[y][x]) )
                else:
                    break


        sorted_weights = sorted(containers, key=lambda x: x[0])


        buffer = Buffer()
        
        start_y=0
        start_x = 23
        for weight, container in sorted_weights:
            print("Move container at ship location " + str(container.pos[1]) + "," + str(container.pos[0]) + " to buffer " + str(start_y) + "," + str(start_x) )
            self.moves.append([['ship to ship exit'], [[container.pos[1],container.pos[0]], [8,0]]])
            print(type(container.pos[1]))
            dist, moves = self.initial.find_distance([container.pos[1], container.pos[0]],[start_y, start_x])
            dist, sub_move = self.initial.find_distance([container.pos[1], container.pos[0]],[start_y, start_x])
            self.sub_moves.append(sub_move)



            self.initial.shipgrid[container.pos[1]][ container.pos[0]] = 0 
            buffer.grid[start_y][start_x] = container 
            container.pos = (start_x, start_y)
            
            start_y+=1
            if start_y == 4:
                start_x-=1
                start_y = 0

        
        
        sift_y = 0
        sift_x = 5

        sorted_weights = sorted(containers, key=lambda x: x[0], reverse=True)


        sift_increment = 1
        sift_shift = True


        num_containers = len(sorted_weights)
        containers_moved = 0

        i = 0
        while containers_moved < num_containers:
            if isinstance(buffer.grid[start_y][start_x], Cargo):
                container = buffer.grid[start_y][start_x]
                print("Move container at buffer location " + str(container.pos[1]) + "," + str(container.pos[0]) + " to ship " + str(sift_y) + "," + str(sift_x) )
                self.initial.shipgrid[sift_y][ sift_x] = container 
                buffer.grid[container.pos[1]][container.pos[0]] = 0 
                container.pos = (sift_x, sift_y)
                if sift_shift:
                    sift_x += sift_increment
                    sift_increment +=1
                    sift_shift = False
                else:
                    sift_x -= sift_increment
                    sift_increment +=1
                    sift_shift = True
                containers_moved+=1
            start_y-=1
            if start_y < 0:
                start_y = 3
                start_x+=1
            

    def update_manifest(self):
        print_grid(self.initial.shipgrid)

        f = open("../static/manifest" + self.input_file[:len(self.input_file)-4]+"OUTBOUND.txt", "w")

        for y in range(8):
            for x in range(12):
                x_zeros = + 2-len(str(x))
                
                if isinstance(self.initial.shipgrid[y][x],Cargo):
                    weight_zeros = 5-len(str(self.initial.shipgrid[y][x].weight))
                    f.write("[0"+str(y)+","+ x_zeros*str("0")+str(x)+"], {"+weight_zeros*str("0") + str(self.initial.shipgrid[y][x].weight)+"}, "+str(self.initial.shipgrid[y][x].container_name)[2:len(self.initial.shipgrid[y][x].container_name)] + '\n')
                elif self.initial.shipgrid[y][x] == 0:
                    f.write("[0"+str(y)+","+  x_zeros*str("0")+str(x)+"], {00000}, UNUSED\n")
                elif self.initial.shipgrid[y][x] == -1:
                    f.write("[0"+str(y)+"," + x_zeros*str("0")+str(x)+"], {00000}, NAN\n")
        
        f.close()