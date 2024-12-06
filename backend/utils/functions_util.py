def get_path(start, goal, load=False):
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
