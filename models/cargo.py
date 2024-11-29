class Cargo:
    def __init__(self, container_name, position):
        self.container_name = container_name
        self.pos = position # [x,y] in the grid
        self.weight = None
        self.heuristic = None # We will start with Manhattan Distance as the heuristic

    def set_weight(self, weight: int):
        self.weight = weight
    
    def get_weight(self):
        return self.weight

    def set_pos(self, pos):
        self.pos = pos
    
    def get_name(self):
        return self.container_name
    
    def set_heuristic(self, goal_pos):
        self.heuristic = abs(goal_pos[0] - self.pos[0]) + abs(goal_pos[1] - self.pos[1])

    def get 