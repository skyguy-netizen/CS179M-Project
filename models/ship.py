class Ship:
    def __init__(self, shipgrid):
        # This grid will be 12 x 8 or whatever is the ship size
        # Each entry will be of object Cargo
        self.shipgrid = shipgrid

    def get_container_pos_by_name(self, container_name: str) -> tuple[int, int]:
        # Search from top to bottom, to get the topmost container
        for i in range(11, -1, -1): # Will loop from 11 to 0
            for j in range(8, -1, -1):
                if self.shipgrid[i][j].get_name() == container_name:
                    return (i, j)
                
        return (-1, -1) # Not found in the ship

