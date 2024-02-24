import random

cell = 0
wall_cell = 1
unv = 5

def init_maze(size: int):
    maze = []
    for y in range(size):
        maze.append([])
        for x in range(size):
            maze[y].append(unv)
    return maze

def maze_gen(plot):
    global cell, wall, unv
    maze = init_maze(plot.size)
    wall_list = []
    
    if plot.size <= 5 :
        return None
    
    height = plot.size
    width = plot.size
    starting_height = int(random.random()*height)
    starting_width = int(random.random()*width)
    
    if starting_height == 0:
        starting_height += 1
    if starting_height == height-1:
        starting_height -= 1
    
    if starting_width == 0:
        starting_width += 1
    if starting_width == width-1:
        starting_width -= 1
    
    # Initial Cell
    maze[starting_height][starting_width] = cell
    set_surrounding_walls(maze, wall_list, starting_height, starting_width)
    
    while (wall_list):
        # Pick a random wall
        rand_wall = wall_list[int(random.random()*len(wall_list))-1]

        # Check if it is a left wall
        if (rand_wall[1] != 0):
            if (maze[rand_wall[0]][rand_wall[1]-1] == unv and maze[rand_wall[0]][rand_wall[1]+1] == cell):
                # Find the number of surrounding cells
                s_cells = surroundingCells(maze, rand_wall)

                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = cell

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != cell):
                            maze[rand_wall[0]-1][rand_wall[1]] = wall_cell
                        if ([rand_wall[0]-1, rand_wall[1]] not in wall_list):
                            wall_list.append([rand_wall[0]-1, rand_wall[1]])


                    # Bottom cell
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != cell):
                            maze[rand_wall[0]+1][rand_wall[1]] = wall_cell
                        if ([rand_wall[0]+1, rand_wall[1]] not in wall_list):
                            wall_list.append([rand_wall[0]+1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):	
                        if (maze[rand_wall[0]][rand_wall[1]-1] != cell):
                            maze[rand_wall[0]][rand_wall[1]-1] = wall_cell
                        if ([rand_wall[0], rand_wall[1]-1] not in wall_list):
                            wall_list.append([rand_wall[0], rand_wall[1]-1])

                # Delete wall
                for wall in wall_list:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        wall_list.remove(wall)
                continue

        # Check if it is an upper wall
        if (rand_wall[0] != 0):
            if (maze[rand_wall[0]-1][rand_wall[1]] == unv and maze[rand_wall[0]+1][rand_wall[1]] == cell):

                s_cells = surroundingCells(maze, rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = cell

                    # Mark the new walls
                    # Upper cell
                    if (rand_wall[0] != 0):
                        if (maze[rand_wall[0]-1][rand_wall[1]] != cell):
                            maze[rand_wall[0]-1][rand_wall[1]] = wall_cell
                        if ([rand_wall[0]-1, rand_wall[1]] not in wall_list):
                            wall_list.append([rand_wall[0]-1, rand_wall[1]])

                    # Leftmost cell
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != cell):
                            maze[rand_wall[0]][rand_wall[1]-1] = wall_cell
                        if ([rand_wall[0], rand_wall[1]-1] not in wall_list):
                            wall_list.append([rand_wall[0], rand_wall[1]-1])

                    # Rightmost cell
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != cell):
                            maze[rand_wall[0]][rand_wall[1]+1] = wall_cell
                        if ([rand_wall[0], rand_wall[1]+1] not in wall_list):
                            wall_list.append([rand_wall[0], rand_wall[1]+1])

                # Delete wall
                for wall in wall_list:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        wall_list.remove(wall)
                continue

        # Check the bottom wall
        if (rand_wall[0] != height-1):
            if (maze[rand_wall[0]+1][rand_wall[1]] == unv and maze[rand_wall[0]-1][rand_wall[1]] == cell):

                s_cells = surroundingCells(maze, rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = cell

                    # Mark the new walls
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != cell):
                            maze[rand_wall[0]+1][rand_wall[1]] = wall_cell
                        if ([rand_wall[0]+1, rand_wall[1]] not in wall_list):
                            wall_list.append([rand_wall[0]+1, rand_wall[1]])
                    if (rand_wall[1] != 0):
                        if (maze[rand_wall[0]][rand_wall[1]-1] != cell):
                            maze[rand_wall[0]][rand_wall[1]-1] = wall_cell
                        if ([rand_wall[0], rand_wall[1]-1] not in wall_list):
                            wall_list.append([rand_wall[0], rand_wall[1]-1])
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != cell):
                            maze[rand_wall[0]][rand_wall[1]+1] = wall_cell
                        if ([rand_wall[0], rand_wall[1]+1] not in wall_list):
                            wall_list.append([rand_wall[0], rand_wall[1]+1])

                # Delete wall
                for wall in wall_list:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        wall_list.remove(wall)
                continue

        # Check the right wall
        if (rand_wall[1] != width-1):
            if (maze[rand_wall[0]][rand_wall[1]+1] == unv and maze[rand_wall[0]][rand_wall[1]-1] == cell):

                s_cells = surroundingCells(maze, rand_wall)
                if (s_cells < 2):
                    # Denote the new path
                    maze[rand_wall[0]][rand_wall[1]] = cell

                    # Mark the new walls
                    if (rand_wall[1] != width-1):
                        if (maze[rand_wall[0]][rand_wall[1]+1] != cell):
                            maze[rand_wall[0]][rand_wall[1]+1] = wall_cell
                        if ([rand_wall[0], rand_wall[1]+1] not in wall_list):
                            wall_list.append([rand_wall[0], rand_wall[1]+1])
                    if (rand_wall[0] != height-1):
                        if (maze[rand_wall[0]+1][rand_wall[1]] != cell):
                            maze[rand_wall[0]+1][rand_wall[1]] = wall_cell
                        if ([rand_wall[0]+1, rand_wall[1]] not in wall_list):
                            wall_list.append([rand_wall[0]+1, rand_wall[1]])
                    if (rand_wall[0] != 0):	
                        if (maze[rand_wall[0]-1][rand_wall[1]] != cell):
                            maze[rand_wall[0]-1][rand_wall[1]] = wall_cell
                        if ([rand_wall[0]-1, rand_wall[1]] not in wall_list):
                            wall_list.append([rand_wall[0]-1, rand_wall[1]])

                # Delete wall
                for wall in wall_list:
                    if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                        wall_list.remove(wall)
                continue

        # Delete the wall from the list anyway
        for wall in wall_list:
            if (wall[0] == rand_wall[0] and wall[1] == rand_wall[1]):
                wall_list.remove(wall)

    # Mark the remaining unvisited cells as walls
    for i in range(0, height):
        for j in range(0, width):
            if (maze[i][j] == unv):
                maze[i][j] = wall_cell
    return maze

def set_surrounding_walls(maze:list, wall_list: list, st_height: int, st_width: int):
    wall_list.append([st_height-1, st_width])
    wall_list.append([st_height, st_width-1])
    wall_list.append([st_height, st_width+1])
    wall_list.append([st_height+1, st_width])
    
    maze[st_height-1][st_width] = wall_cell
    maze[st_height][st_width-1] = wall_cell
    maze[st_height][st_width+1] = wall_cell
    maze[st_height+1][st_width] = wall_cell

def surroundingCells(maze, rand_wall):
    global cell, wall, unv
    s_cells = 0
    if (maze[rand_wall[0]-1][rand_wall[1]] == cell):
        s_cells += 1
    if (maze[rand_wall[0]+1][rand_wall[1]] == cell):
        s_cells += 1
    if (maze[rand_wall[0]][rand_wall[1]-1] == cell):
        s_cells +=1
    if (maze[rand_wall[0]][rand_wall[1]+1] == cell):
        s_cells += 1
    return s_cells