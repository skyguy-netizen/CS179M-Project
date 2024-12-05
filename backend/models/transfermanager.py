from typing import List
from backend.models.cargo import Cargo
from backend.models.ship import Ship

class TransferManager:
    def __init__(self, load_list: List[Cargo], unload_list: List[Cargo], ship_grid: Ship):
        self.load_list = load_list # Load list should have cargo object and the target for the cargo object
        self.unload_list = unload_list
        self.ship_grid = ship_grid
        self.container_log = []
        self.time_estimate = 0

    def set_goal_locations(self,):
        for cargo in self.unload_list:
            cargo.set_heuristic_score((8, 0)) # This is the pink box
        
        for cargo in self.load_list:
            cargo.set_pos((8, 0))
            cargo.set_heuristic_score((0,0))
        
    def manhattan_distance_calculation(self,start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def unload(self, cargo: Cargo):
        while not self.ship_grid.can_move_container(cargo.pos):
            blocking_position = self.ship_grid.top_most_container(cargo.pos[1])
            blocking_cargo = self.ship_grid.shipgrid[blocking_position[0]][blocking_position[1]]
            self.move_blocking_container(blocking_cargo)

        # Move container to goal
        start = cargo.pos
        goal = (8, 0)
        move_cost = self.manhattan_distance_calculation(start,goal) + 2
        path = self.ship_grid.move_container(start, goal)
        cargo.pos = goal
        self.update_log(cargo, start, move_cost, path, load=False)

    def load(self, cargo: Cargo):
        # Here we simply find the closest position to load it
        for i in range(12):
            open_pos = self.ship_grid.find_shortest_column(i)
            if open_pos != (None, None):
                path = [9,9]
                move_cost = self.manhattan_distance_calculation((8,0), open_pos) + 2
                self.ship_grid.shipgrid[open_pos[0]][open_pos[1]] = cargo
                cargo.pos = open_pos
                self.update_log(cargo,open_pos,move_cost,path)
                return
        

    def move_blocking_container(self, cargo: Cargo):
        curr_pos = cargo.pos
        if curr_pos[1] >= len(self.ship_grid.shipgrid[1]) - 1:
            goal_column = curr_pos[1] - 1
        else:
            goal_column = curr_pos[1] + 1
        new_pos = self.ship_grid.find_shortest_column(goal_column)
        move_cost = self.manhattan_distance_calculation(curr_pos,new_pos)
        path = self.ship_grid.move_container(curr_pos, new_pos)
        self.update_log(cargo,curr_pos,move_cost, path, load=False, move_blocking=True)

    def print_grid(self):
        cell_width = 10
        for row in self.ship_grid.shipgrid:
            print(
                " | ".join(
                    f"{str(cell):^{cell_width}}" if cell is not None else f"{'None':^{cell_width}}"
                    for cell in row
                )
            )

    def transfer_algorithm(self):
        # Sort lists based on g_score + heuristic
        self.unload_list.sort(key=lambda c: c.g_score + c.heuristic_score, reverse=True)
        self.load_list.sort(key=lambda c: c.g_score + c.heuristic_score, reverse=True)

        self.print_grid()

        while self.unload_list or self.load_list:
            # Process UnloadList
            if self.unload_list:
                cargo = self.unload_list.pop()
                print(f"Unloading {cargo.container_name} from {cargo.pos}.")
                self.unload(cargo)
                print(f"Unloaded {cargo.container_name} from {cargo.pos}.")
                self.print_grid()
                print("\n")

            # Process LoadList
            if self.load_list:
                cargo = self.load_list.pop()
                print(f"Loading {cargo.container_name}")
                self.load(cargo)
                print(f"Loaded {cargo.container_name}")
                self.print_grid()
                print("\n")

        print(f"\n Total Time Estimate: {self.time_estimate} minutes")


    def update_log(self, cargo: Cargo, start, cost, path, load=True, move_blocking = False): 
        path_trace = "->".join(map(str,[start] + path))
        if move_blocking:
            self.container_log.append(f"Move {cargo.get_name()} from {start} to {cargo.get_pos()}, Cost: {cost} minutes, Path taken: {path_trace}") 
        elif load:
            self.container_log.append(f"Loaded {cargo.get_name()} from truck to {cargo.get_pos()}, Cost: {cost} minutes, Path taken: {path_trace}")
        else:
            self.container_log.append(f"Move {cargo.get_name()} from {start} to truck, Cost: {cost} minutes, Path taken: {path_trace}") 
        self.time_estimate += cost

        
    