import datetime


def get_path(start, goal, load=False,):
    x1, y1 = start
    x2, y2 = goal
    print("Start ", start, "Goal", goal)
    path = [(x1, y1)]
    if load:
        # if y1 < y2:  # Moving "right" (increasing y)
        for y in range(y1 + 1, y2 + 1):
            path.append((x1, y))
        # elif y1 > y2:  # Moving "left" (decreasing y)
        # for y in range(y1 - 1, y2 - 1, -1):
        #     path.append((x2, y))

        # if x1 < x2:  # Moving "up" (increasing x)
        #     for x in range(x1 + 1, x2 + 1):
        #         path.append((x, y1))
        # elif x1 > x2:  # Moving "down" (decreasing x)
        for x in range(x1 - 1, x2 - 1, -1):
            path.append((x, y2))
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
    path = []  # Initialize the path
    num_rows = len(ship_grid)
    num_columns = len(ship_grid[0])


    best_path = None
    smallest_vertical_diff = float('inf')

    for offset in [-1,1]:  # Check both adjacent columns
        adjacent_column = y1 + offset
        if 0 <= adjacent_column < num_columns:  
            for x in range(num_rows):  # Search
                if ship_grid[x][adjacent_column] is None: 
                    is_valid = all(ship_grid[row][adjacent_column] is not None for row in range(x))
                    if is_valid:
                        # Generate the path to this position
                        temp_path = [(x1, y1)]
                        
                        temp = x1
                        # Vertical movement up first if higher then left or right then down if needed
                        if x > x1:
                            temp = x
                            if x1 == 3 and y1 == 4:
                                print(f"in here {x} {adjacent_column}")
                            for move_x in range (x1, x + 1, +1):
                                if temp_path[-1] == (x, y1):
                                    continue
                                temp + 1
                                if temp_path[-1] == (move_x,y1):
                                    continue
                                else:
                                    temp_path.append((move_x, y1))

                        # Horizontal movement
                        if adjacent_column > y1:  # Moving right
                            for y in range(y1 + 1, adjacent_column + 1):
                                if temp_path[-1] == (temp,y):
                                    continue
                                else:
                                    temp_path.append((temp, y))
                        elif adjacent_column < y1:  # Moving left
                            for y in range(y1 - 1, adjacent_column - 1, -1):
                                if temp_path[-1] == (temp,y):
                                    continue
                                else:
                                    temp_path.append((temp, y))

                        if x < x1:      
                            for move_x in range(x1, x - 1, -1):  # Move down
                                if temp_path and temp_path[-1] == (x, adjacent_column):
                                    continue
                                if temp_path[-1] == (move_x,adjacent_column):
                                    continue
                                else:
                                    temp_path.append((move_x, adjacent_column))

                        # Calculate distance 
                        vertical_diff = abs(x1 - x)

                        # Choose the column with the smallest vertical difference
                        if vertical_diff < smallest_vertical_diff:
                            smallest_vertical_diff = vertical_diff
                            best_path = temp_path       
                           

                    break 



    if best_path is not None:
        return best_path


    for x in range(x1, num_rows):
        if ship_grid[x][y1] is None: 
            is_valid = all(
                ship_grid[row][y1] not in (None, "Blocked") for row in range(x)
            )
            if is_valid:
                for move_x in range(x1, x + 1): 
                    path.append((move_x, y1))
                break

    return path



def get_curr_time(): #Return something in this format "YYYY-MM-DD HH-MM   "
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M\t")