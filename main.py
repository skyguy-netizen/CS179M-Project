# from models.cargo import Cargo
# from models.transfermanager import TransferManager
# from models.ship import Ship


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


from models.cargo import Cargo
from models.ship import Ship
from models.transfermanager import TransferManager

def main():
    # Initialize a sample ship grid (8x12 grid)
    ship_grid = [[None for _ in range(12)] for _ in range(8)]

    # Add some cargo to the grid
    ship_grid[0][3] = Cargo("Samsung", (0, 3))
    ship_grid[1][3] = Cargo("Apple", (1, 3))
    ship_grid[2][3] = Cargo("LG", (2, 3))  # Blocking cargo
    ship_grid[0][6] = Cargo("Sony", (0, 6))

    # Initialize the Ship object
    ship = Ship(ship_grid)

    # Create load and unload lists
    load_list = [
        Cargo("Panasonic", None),  # To be loaded at (8, 0)
        Cargo("Toshiba", None),    # To be loaded at (8, 0)
    ]

    unload_list = [
        ship_grid[0][3],  # Samsung at (7, 3)
        ship_grid[1][3],  # Apple at (6, 3)
    ]

    # Initialize TransferManager
    tm = TransferManager(load_list, unload_list, ship)

    # Set goal locations for all cargos
    tm.set_goal_locations()

    # Run the transfer algorithm
    print("\n--- Starting Transfer Algorithm ---")
    tm.transfer_algorithm()
    print("\n--- Transfer Completed ---")

    # Print the log of operations
    print("\n--- Operation Log ---")
    for log in tm.container_log:
        print(log)

if __name__ == "__main__":
    main()
