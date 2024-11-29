from cargo import Cargo
from ship import Ship
import math
import heapq
class TransferManager:
    def __init__(self, load_list, unload_list, ship_grid: Ship):
        self.load_list = load_list
        self.unload_list = unload_list
        self.ship_grid = ship_grid


    def sort_lists(self):
        for cargo_name in self.load_list


    def run_algorithm(optimized_transfer_list):
        #algorithm to perform on optimzed transferlist (A*)
        print("Running Algorithm")
    
    def optimize_transfer_list(transfer_list):
        #optimizes list to be ran on algorithm
        print ("Optimizing TransferList")

    # checking edge cases to see if valid opeeration on 8 X 12 grid with 0 indexing
    # should also check if there is currently a container in the surrounding position
    def is_valid_move(self, row, col):

    
    def is_valid_left(j):
        if (j - 1 < 0):
            return False
        else:
            if 
            return True
    def is_valid_right(j):
        if (j + 1 > 11):
            return False
        else:
            return True
    def is_valid_up(i):
        if (i - 1 < 0):
            return False
        else:
            return True
    def is_valid_down(i):
        if (i + 1 > 7):
            return False
        else:
            return True 

    





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
 
 
