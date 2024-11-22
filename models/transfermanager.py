from cargo import Cargo
import math
import heapq
class TransferManager:
    def transfer_list(userIn):
        #read in and instantiate transferlist using cargo
        #not sure how we want to read in the input from operator
        transfer = []   #transfer is a list of cargo objects
        transfer.append(userIn) #userIn is the cargo object to be added to the transferlist by the operator
        print("TransferList:", transfer)

    def run_algorithm(optimized_transfer_list):
        #algorithm to perform on optimzed transferlist (A*)
        print("Running Algorithm")
    
    def optimize_transfer_list(transfer_list):
        #optimizes list to be ran on algorithm
        print ("Optimizing TransferList")

    # checking edge cases to see if valid opeeration on 8 X 12 grid with 0 indexing
    # should also check if there is currently a container in the surrounding position
    def is_valid_left(j):
        if (j - 1 < 0):
            return False
        else:
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
 
 
