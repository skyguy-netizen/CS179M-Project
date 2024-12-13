import copy
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from utils.functions_util import get_path, get_curr_time
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
        print()


class Balance:
    def __init__ (self, ship: Ship, input_file, log_file):
        self.initial = ship
        self.input_file = input_file
        self.moves = []
        self.sub_moves = []
        self.process = []

        if not log_file:
            raise Exception("Log file required!!")
        self.log_file = log_file
        self.total_time = 0

    def check_balance(self):
        return self.initial.goal_state

    
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
        self.update_log()

    def balance_iter(self):
        print("itera bal")
        grids_states = []
        past_states = set()


        containers = []
        for x in range(0,12):
            for y in range(0,8):
                if isinstance(self.initial.shipgrid[y][x], Cargo):
                    containers.append(self.initial.shipgrid[y][x])
                    print(self.initial.shipgrid[y][x].container_name)
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
                print_grid(self.initial.shipgrid)
                for i in range(len(self.moves)):
                    self.process.append([str(current_grid.names[i]), current_grid.distances[i], current_grid.total_moves[i]])

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

                    

            for container_y, container_x in container_location:
                if current_grid.shipgrid[container_y+1][container_x] != 0:
                    continue
                for space_y, space_x in empty_spaces:

                    if space_x == container_x:
                        continue

                    new_grid = copy.deepcopy(current_grid)
                    new_grid.shipgrid[space_y][space_x] = current_grid.shipgrid[container_y][container_x]
                    new_grid.shipgrid[container_y][container_x] = 0
                    
                    dist = current_grid.find_distance([container_y, container_x],[space_y, space_x])
                    if dist == -1:
                        continue

                    moves=dist[1]
                    dist=dist[0]
                    
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
        id=0
        for x in range(0,12):
            for y in range(0,8):
                if isinstance(self.initial.shipgrid[y][x], Cargo):
                    self.initial.shipgrid[y][x].id = id
                    containers.append((self.initial.shipgrid[y][x].weight, self.initial.shipgrid[y][x]) )
                    id+=1
                else:
                    break
       
        sorted_weights = sorted(containers, key=lambda x: x[0], reverse=True)
    

        positions = {}
        sift_y = 0
        sift_x = 5
        

        sift_increment = 1
        sift_shift = True

        
        num_containers = 0
     
        while num_containers < len(sorted_weights):
            positions[num_containers] = [sift_y, sift_x]

            if sift_shift:
                sift_x += sift_increment
            else:
                sift_x -= sift_increment
            sift_increment+=1
            sift_shift =  not sift_shift
            
            

            num_containers+=1
       



        grids_states = []
        past_states = set()

        containers = []
        for x in range(0,12):
            for y in range(0,8):
                if isinstance(self.initial.shipgrid[y][x], Cargo):
                    containers.append(self.initial.shipgrid[y][x])
                elif self.initial.shipgrid[y][x] == 0:
                    break

        self.initial.gx= 0
        self.initial.fx = 0
        grids_states.append((self.initial.fx, self.initial))
        self.initial.compress()
        past_states.add(self.initial.compression)

        id = 0
        while True:
    
            if len(grids_states) == 0:
                break

            current_grid = grids_states[0][1]
            del grids_states[0]

            if current_grid.goal_state: 
                self.initial = copy.deepcopy(current_grid)

                self.moves = current_grid.moves
                self.sub_moves = current_grid.total_moves

                for i in range(len(self.moves)):
                    self.process.append([current_grid.names[i], current_grid.distances[i], current_grid.total_moves[i]])
             

                print_grid(current_grid.shipgrid)
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

                    new_grid.id = id
                    id+=1

                    new_grid.hx = 0
                    for x in range(0,12):
                        for y in range(0,8):
                            
                            if isinstance(new_grid.shipgrid[y][x], Cargo) :
                            
                                if not (positions[new_grid.shipgrid[y][x].id] == [y,x]):
                                    new_grid.hx += 10
                            elif new_grid.shipgrid[y][x] == 0:
                                break
                
                    
                    new_grid.fx = new_grid.gx + new_grid.hx
                    if new_grid.hx == 0:
                        new_grid.goal_state = True
                    


                    new_grid.compress()

                    if not new_grid.compression in past_states:
                        grids_states.append((new_grid.fx,new_grid))

                        past_states.add(new_grid.compression)
           

            grids_states= sorted(grids_states, key=lambda x: x[0])
        



    def update_manifest(self):
        f = open("../static/manifest/" + self.input_file[:len(self.input_file)-4]+"OUTBOUND.txt", "w")

        for y in range(8):
            for x in range(12):
                x_zeros = + 2-len(str(x))
                
                if isinstance(self.initial.shipgrid[y][x],Cargo):
                    weight_zeros = 5-len(str(self.initial.shipgrid[y][x].weight))
                    f.write("[0"+str(y)+","+ x_zeros*str("0")+str(x)+"], {"+weight_zeros*str("0") + str(self.initial.shipgrid[y][x].weight)+"}, "+str(self.initial.shipgrid[y][x].container_name)[:len(self.initial.shipgrid[y][x].container_name)] + '\n')
                elif self.initial.shipgrid[y][x] == 0:
                    f.write("[0"+str(y)+","+  x_zeros*str("0")+str(x)+"], {00000}, UNUSED\n")
                elif self.initial.shipgrid[y][x] == -1:
                    f.write("[0"+str(y)+"," + x_zeros*str("0")+str(x)+"], {00000}, NAN\n")
        f.close()

    

    def update_log(self):
        with open(self.log_file, 'a') as log:
            for i in range(len(self.moves)):
                log.write(f"{get_curr_time()}Move {self.process[i][0][:-1]} from {self.moves[i][0]} to {self.moves[i][1]}, Cost: {self.process[i][1]} minutes\n")
                self.total_time += self.process[i][1]

            
        

        
        

