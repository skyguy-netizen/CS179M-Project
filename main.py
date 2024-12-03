from models.cargo import Cargo
from models.transfermanager import TransferManager
from models.ship import Ship


# Example grid setup
ship_grid_data = [
    [Cargo("Test", (0, 0)), Cargo("Samsung", (0, 1)), Cargo("Apple", (0, 2)), None, None, None, None, None, None, None, None, None],
    [None, Cargo("Sony", (1, 1)), None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None],
]

ship_grid = Ship(ship_grid_data)

# Create load and unload lists
load_list = [Cargo("LG", (8, 0)), Cargo("Panasonic", (8, 0))]
unload_list = [Cargo("Samsung", (0, 1)), Cargo("Apple", (0, 2)), Cargo("Test", (0, 0))]

# Initialize TransferManager
tm = TransferManager(load_list, unload_list, ship_grid)

# Process cargo lists
tm.transfer_algorithm()  # Truck position and load goal
