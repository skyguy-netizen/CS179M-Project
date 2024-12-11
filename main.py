from copy import deepcopy

from backend.models.cargo import Cargo
from backend.models.ship import Ship
from backend.utils.manifest_handler import set_file
from backend.models.transfermanager import TransferManager

def main():
    # Initialize a sample ship grid (8x12 grid)
    ship_grid = [[None for _ in range(12)] for _ in range(8)]
    input_file = ('SilverQueen.txt')
    ship = set_file('SilverQueen.txt')
    ship_grid = ship.shipgrid

    # Create load and unload lists
    load_list = [
        Cargo("Nat", weight = 153),  
        # Cargo("Rat", int(2321)),      
    ]

    unload_list = [
        # deepcopy(ship_grid[0][3]),  
        deepcopy(ship_grid[0][1]),  
    ]

    tm = TransferManager(load_list, unload_list, ship)

    tm.set_goal_locations()

    tm.transfer_algorithm()
    output_file_name = input_file.rsplit('.', 1)[0] + "OUTBOUND.txt"
    tm.update_manifest(output_file_name)
    tm.print_moves()
    print("\n--- Operation Log ---")
    for log in tm.container_log:
        print(log)

if __name__ == "__main__":
    main()
