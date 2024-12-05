# from models.cargo import Cargo
# from models.transfermanager import TransferManager
# from models.ship import Ship
from copy import deepcopy


# # Example grid setup
# ship_grid_data = [
#     [Cargo("Test", (0, 0)), Cargo("Samsung", (0, 1)), Cargo("Apple", (0, 2)), None, None, None, None, None, None, None, None, None],
#     [None, Cargo("Sony", (1, 1)), None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None],
#     [None, None, None, None, None, None, None, None, None, None, None, None],
# ]

# ship_grid = Ship(ship_grid_data)

# # Create load and unload lists
# load_list = [Cargo("LG", (8, 0)), Cargo("Panasonic", (8, 0))]
# unload_list = [Cargo("Samsung", (0, 1)), Cargo("Apple", (0, 2)), Cargo("Test", (0, 0))]

# # Initialize TransferManager
# tm = TransferManager(load_list, unload_list, ship_grid)

# # Process cargo lists
# tm.transfer_algorithm()  # Truck position and load goal


from backend.models.cargo import Cargo
from backend.models.ship import Ship
from backend.utils.manifest_handler import set_file
from backend.models.transfermanager import TransferManager

def main():
    # Initialize a sample ship grid (8x12 grid)
    ship_grid = [[None for _ in range(12)] for _ in range(8)]
    
    ship = set_file('SilverQueen.txt')
    ship_grid = ship.shipgrid
    # # Initialize the Ship object
    # ship = Ship(ship_grid)

    # Create load and unload lists
    load_list = [
        Cargo("Natron", None),      
    ]

    unload_list = [
        deepcopy(ship_grid[0][3]),  
        deepcopy(ship_grid[0][1]),  
    ]
    tm = TransferManager(load_list, unload_list, ship)

    tm.set_goal_locations()

    tm.transfer_algorithm()


    print("\n--- Operation Log ---")
    for log in tm.container_log:
        print(log)

if __name__ == "__main__":
    main()
