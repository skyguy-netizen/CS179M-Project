class Cargo:
    def __init__(self, container_name, position = None, weight = None):
        self.container_name = container_name
        self.pos = position # [x,y] in the grid
        self.weight = weight
        self.heuristic = None # We will start with Manhattan Distance as the heuristic
        self.g_score = 0
        self.f_score = 0

    def __repr__(self):
        return self.container_name[:3]

    def set_weight(self, weight: int):
        self.weight = weight
    
    def get_weight(self):
        return self.weight

    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self): 
        return self.pos
    
    def get_name(self):
        return self.container_name
    
    def set_heuristic_score(self, goal_pos):
        self.heuristic_score = abs(goal_pos[0] - self.pos[0]) + abs(goal_pos[1] - self.pos[1])

    def set_g_score(self, g_score):
        self.g_score = g_score

    def get_f_score(self):
        return self.g_score + self.heuristic_score
    
    def get_g_score(self):
        return self.g_score

    def get_heuristic_score(self):
        return self.heuristic_score