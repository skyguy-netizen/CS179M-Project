class Cargo:
    def __init__(self, name, weight, position):
        self.name = name
        self.weight = weight
        self.position = position  # (row, col)

    def __repr__(self):
        return f"{self.name} at {self.position}"


def count_obstructions(ship_grid, position):
    """
    Counts the number of containers above the given position in the ship grid.
    :param ship_grid: 2D array representing the ship grid.
    :param position: Tuple (row, col) of the target container.
    :return: Number of containers above the target position.
    """
    row, col = position
    obstructions = 0
    for r in range(row + 1, len(ship_grid)):
        if ship_grid[r][col] != "UNUSED":
            obstructions += 1
    return obstructions

def find_all_instances(ship_grid, container_name):
    """
    Finds all positions of a container name in the ship grid.
    :param ship_grid: 2D array representing the ship grid.
    :param container_name: Name of the container to locate.
    :return: List of positions (row, col) where the container is found.
    """
    positions = []
    for row in range(len(ship_grid)):
        for col in range(len(ship_grid[row])):
            if ship_grid[row][col] == container_name:
                positions.append((row, col))
    return positions


def resolve_ship_duplicates(transfer_list, ship_grid, pink_cell):
    """
    Resolves duplicates by selecting the easiest-to-transfer instance for each container in the transfer list.
    :param transfer_list: List of Cargo objects to be deduplicated.
    :param ship_grid: 2D array representing the ship grid.
    :param pink_cell: Tuple (row, col) representing the pink cell for exit.
    :return: List of Cargo objects with the easiest instance selected for each.
    """
    resolved_list = []

    for cargo in transfer_list:
        all_positions = find_all_instances(ship_grid, cargo.name)

        # Select the easiest position for this cargo
        easiest_position = min(
            all_positions,
            key=lambda pos: (
                count_obstructions(ship_grid, pos),  # Fewest obstructions
                abs(pos[0] - pink_cell[0]) + abs(pos[1] - pink_cell[1])  # Shortest Manhattan distance
            )
        )
        # Create a new Cargo object with the selected position
        resolved_list.append(Cargo(cargo.name, cargo.weight, easiest_position))

    return resolved_list


def optimize_transfer_list_with_ship_duplicates(transfer_list, ship_grid, pink_cell):
    """
    Optimizes the transfer list, accounting for duplicates in the ship grid.
    :param transfer_list: List of Cargo objects.
    :param ship_grid: 2D array representing the ship grid.
    :param pink_cell: Tuple (row, col) representing the pink cell for exit.
    :return: Optimized list of Cargo objects.
    """
    # Resolve duplicates in the ship grid
    resolved_list = resolve_ship_duplicates(transfer_list, ship_grid, pink_cell)

    # Sort the resolved list based on ease of transfer
    def difficulty_score(cargo):
        row, col = cargo.position
        obstructions = count_obstructions(ship_grid, (row, col))
        manhattan_distance = abs(row - pink_cell[0]) + abs(col - pink_cell[1])
        return obstructions, manhattan_distance

    return sorted(resolved_list, key=difficulty_score)


# Ship grid with duplicates
ship_grid = [
    ["BoxA", "UNUSED", "BoxB", "UNUSED"],
    ["BoxC", "BoxA", "BoxB", "UNUSED"],
    ["BoxA", "UNUSED", "BoxC", "UNUSED"],
]

# Transfer list (duplicates expected on the ship)
transfer_list = [
    Cargo("BoxA", 100, None),  # Position will be resolved
    Cargo("BoxB", 200, None),  # Position will be resolved
    Cargo("BoxC", 300, None),  # Position will be resolved
]

# Define pink cell (exit point for the ship)
pink_cell = (0, 1)

for a in ship_grid:
    print(a)

# Optimize the transfer list
optimized_list = optimize_transfer_list_with_ship_duplicates(transfer_list, ship_grid, pink_cell)
print("Optimized Transfer List:", optimized_list)

# Next steps, say we want the k best duplicates