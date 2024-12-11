import datetime


def get_path(start, goal, load=False,):
    x1, y1 = start
    x2, y2 = goal
    path = [(x1, y1)]
    if load:
        if y1 < y2:  # Moving "right" (increasing y)
            for y in range(y1 + 1, y2 + 1):
                path.append((x2, y))
        elif y1 > y2:  # Moving "left" (decreasing y)
            for y in range(y1 - 1, y2 - 1, -1):
                path.append((x2, y))

        if x1 < x2:  # Moving "up" (increasing x)
            for x in range(x1 + 1, x2 + 1):
                path.append((x, y1))
        elif x1 > x2:  # Moving "down" (decreasing x)
            for x in range(x1 - 1, x2 - 1, -1):
                path.append((x, y1))
    else:    
        if x1 < x2:  # Moving "up" (increasing x)
            for x in range(x1 + 1, x2 + 1):
                path.append((x, y1))
        elif x1 > x2:  # Moving "down" (decreasing x) 
            for x in range(x1 - 1, x2 - 1, -1):
                path.append((x, y1))

        if y1 < y2:  # Moving "right" (increasing y)
            for y in range(y1 + 1, y2 + 1):
                path.append((x2, y))
        elif y1 > y2:  # Moving "left" (decreasing y)
            for y in range(y1 - 1, y2 - 1, -1):
                path.append((x2, y))
    return path


def get_path_for_blocking(start, ship_grid):
   
    x1, y1 = start  # Current position of the blocking container
    path = [(x1, y1)]  # Initialize the path
    num_rows = len(ship_grid)
    num_columns = len(ship_grid[0])

    # Initialize variables to store the best target
    # best_target_column = None
    # best_target_row = None
    best_path = None
    smallest_vertical_diff = float('inf')

    for offset in [-1, 1]:  # Check both adjacent columns
        adjacent_column = y1 + offset
        if 0 <= adjacent_column < num_columns:  # Ensure the column is within bounds
            for x in range(num_rows):  # Search from bottom to top
                if ship_grid[x][adjacent_column] is None:  # Found an open space
                    is_valid = all(ship_grid[row][adjacent_column] is not None for row in range(x))
                    if is_valid:
                        # Generate the path to this position
                        temp_path = []

                        # Horizontal movement
                        if adjacent_column > y1:  # Moving right
                            for y in range(y1 + 1, adjacent_column + 1):
                                temp_path.append((x1, y))
                        elif adjacent_column < y1:  # Moving left
                            for y in range(y1 - 1, adjacent_column - 1, -1):
                                temp_path.append((x1, y))

                        # Vertical movement
                        for move_x in range(x1, x - 1, -1):  # Move down
                            if temp_path and temp_path[-1] == (move_x, adjacent_column):
                                continue
                            temp_path.append((move_x, adjacent_column))

                         # Calculate the vertical distance (absolute difference)
                        vertical_diff = abs(x1 - x)

                        # Choose the column with the smallest vertical difference
                        if vertical_diff < smallest_vertical_diff:
                            smallest_vertical_diff = vertical_diff
                            # best_target_row = x
                            # best_target_column = adjacent_column
                            best_path = temp_path
                            
                    break 


    # If a valid adjacent column is found, return the best path
    if best_path is not None:
        return path + best_path

    # If no adjacent columns are available, move vertically to the top of the current column
    for x in range(x1, num_rows):
        if ship_grid[x][y1] is None: 
            is_valid = all(
                ship_grid[row][y1] not in (None, "Blocked") for row in range(x)
            )
            if is_valid:
                for move_x in range(x1, x + 1):  # Add vertical movement
                    path.append((move_x, y1))
                break

    return path

def get_curr_time(): #Return something in this format "YYYY-MM-DD HH-MM   "
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M\t")