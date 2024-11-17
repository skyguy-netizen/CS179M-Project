class Cargo:
    def __init__(self, container_name, position):
        self.container_name = container_name
        self.pos = position # [x,y] in the grid
        self.weight = None

    def set_weight(self, weight: int):
        self.weight = weight
    
    def get_weight(self):
        return self.weight

    def set_pos(self, pos):
        self.pos = pos
    
    def get_name(self):
        return self.container_name