from cargo import Cargo
from ship import Ship
import math
import heapq
class TransferManager:
    def __init__(self, load_list, unload_list, ship_grid: Ship):
        self.load_list = load_list
        self.unload_list = unload_list
        self.ship_grid = ship_grid
        self.container_log = []

    def create_transfer_list(self):
        #rows and cols may not work correctly
        for row in range (self.ship.len(self.ship.shipgrid)):
            for col in range (self.ship.len(self.ship.shipgrid[0])):
                cargo = self.ship_grid[row][col]
                if cargo and cargo.container_name in self.load_list:
                    self.unload_list.append(cargo)
        self.unload_list.sort()

    #def sort_lists(self):
    #   for cargo_name in self.load_list

    def goal_locations (self,goal): #second parameter to store goal position
        for cargo in self.unload_list:
            cargo.heuristic = self.manhattan_distance_calculation(cargo.pos, goal)

    def manhattan_distance_calculation (start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    
    def transfer(self):
        while self.unload_list:
            cargo = self.unload_list.pop(0)
    
    def unload (self, cargo):
        while not self.ship.can_move_container(cargo.pos):
            cargo_above = self.ship.top_most_container(cargo.pos[1])
            cargo_object = self.ship_grid[cargo_above[0]][cargo_above[1]]
            self.move_blocking_containers(cargo_object)
        #need to log any moves
        self.update_log(cargo)
        self.ship_grid[cargo.pos[0]][cargo.pos[1]] = None

    def move_blocking_containers (self, cargo):
        curr_pos = cargo.pos
        if curr_pos[1] < len(self.ship_grid[0]) - 1:
            goal_column = curr_pos[1] - 1
        else:
            goal_column = curr_pos[1] + 1
        new_pos = self.ship.find_shortest_column(goal_column)
        self.ship.move_container(curr_pos,new_pos)
        self.update_log(cargo, new_pos)

    def update_log (self,cargo,goal):
        self.container_log.append (f"Move {cargo.container_name} from {cargo.pos} to {goal}")

    def run_algorithm(optimized_transfer_list):
        #algorithm to perform on optimzed transferlist (A*)
        print("Running Algorithm")
    
    def optimize_transfer_list(transfer_list):
        #optimizes list to be ran on algorithm
        print ("Optimizing TransferList")

    def a_star_searching (self,start,goal):
        empty_set = []
        heapq.heappush(empty_set, (0,start))
        original = {}
        start_score = {start: 0}
        final_score = {start: self.manhattan_distance_calculation(start,goal)}

        while empty_set:
            curr = heapq.heappop(empty_set)
            if curr == goal:
                return start_score[curr]
            
            for neighbor in self.ship.find_neighbors(curr):
                curr_score = start_score[curr] + 1
                if neighbor not in start_score or curr_score < start_score[neighbor]:
                    original [neighbor] = curr
                    start_score [neighbor] = curr_score
                    final_score [neighbor] = curr_score + self.manhattan_distance_calculation(neighbor,goal)
                    if neighbor not in [item[1] for item in empty_set]:
                        heapq.heappush(empty_set,(final_score[neighbor], neighbor)) 

    # checking edge cases to see if valid opeeration on 8 X 12 grid with 0 indexing
    # should also check if there is currently a container in the surrounding position
    #def is_valid_move(self, row, col):

    #probably don't need

    # def is_valid_left(j):
    #     if (j - 1 < 0):
    #         return False
    #     else:
    #         return True
    # def is_valid_right(j):
    #     if (j + 1 > 11):
    #         return False
    #     else:
    #         return True
    # def is_valid_up(i):
    #     if (i - 1 < 0):
    #         return False
    #     else:
    #         return True
    # def is_valid_down(i):
    #     if (i + 1 > 7):
    #         return False
    #     else:
    #         return True 

    





def  uniform_cost_search(start, end, board, container):
    # create a priority queue
    queue = []
    # insert the starting index
    queue.append(start)
 
    # map to store visited node
    visited = {}
 
    # cost
    cost = 0
 
    # while the queue is not empty
    while (len(queue) > 0):
 
        # get the top element of the
        queue = sorted(queue)
        p = queue[0]
 
        # pop the element
        del queue[0]
 
        # get the original value
        p[0] *= -1
 
        # check if the element is part of
        # the goal list
        if (p.pos == end.pos):
            return cost
            # if the cost is less
 
            # pop the element
            del queue[-1]
 
            queue = sorted(queue)
            if (count == len(goal)):
                return answer
 
        # check for the non visited nodes
        # which are adjacent to present node

        # if (p[0].is_valid_left()):
        #     queue.append(board.position[i][j-1])
        # if (p[0].is_valid_right()):
        #     queue.append(board.position[i][j+1])
        # if (p[0].is_valid_down()):
        #     queue.append(board.position[i + 1][j])
        # if (p[0].is_valid_up()):
        #     queue.append(board.position[i - 1][j])
 
 
