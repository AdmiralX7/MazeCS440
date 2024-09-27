import heapq
import json
import time


def reconstruct_path(path, curr):
    total_path = [curr]
    while curr in path.keys():
        curr = path[curr]
        total_path.insert(0, curr)
    return total_path


def get_neighbors(cell: tuple, maze):
    x = cell[0]
    y = cell[1]

    # print(maze)

    n_list = []

    # West
    if y > 0:
        n_list.append((x, y - 1))

    # North
    if x > 0:
        n_list.append((x - 1, y))

    # South
    if x < len(maze) - 1:
        n_list.append((x + 1, y))

    # East
    if y < len(maze[0]) - 1:
        n_list.append((x, y + 1))

    return n_list


def heuristic(cell: tuple, goal):
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def a_star(grid_data, start, goal, tie, h_scores=None):
    
    g_score = {start: 0}

    h_score = h_scores

    if h_score is not None and start in h_score:
        f_score = {start: h_score[start] + g_score[start]}
    else:
        f_score = {start: heuristic(start, goal)}

    open_list = []

    close_list = []
    path = {}
    if tie == 'min_g_score':
        heapq.heappush(open_list, (f_score[start], g_score[start], start))
    elif tie == 'max_g_score':
        heapq.heappush(open_list, (f_score[start], -g_score[start], start))

    while len(open_list) != 0:

        curr_cell = heapq.heappop(open_list)[2]

        # print(curr_cell)
        if curr_cell == goal:
            # print(path)

            for cell in close_list:
                if h_score is not None:
                    h_score[cell] = g_score[goal] - g_score[cell]

            return reconstruct_path(path, curr_cell), close_list, h_score
        # if curr_cell not in close_list:
        #     close_list.append(curr_cell)
        close_list.append(curr_cell)

        n_list = get_neighbors(curr_cell, grid_data)

        for neighbor in n_list:

            if grid_data[neighbor[0]][neighbor[1]] == 0 and (neighbor not in close_list and neighbor not in open_list):

                new_cell = neighbor

                if new_cell not in f_score:
                    g_score[new_cell] = float('inf')
                    f_score[new_cell] = float('inf')

                temp_g_score = g_score[curr_cell] + 1
                if h_score is not None and new_cell in h_score:
                    temp_f_score = temp_g_score + h_score[new_cell]
                else:
                    temp_f_score = temp_g_score + heuristic(new_cell, goal)

                if temp_f_score < f_score[new_cell]:
                    # print(new_cell)
                    g_score[new_cell] = temp_g_score

                    f_score[new_cell] = temp_f_score

                    if tie == 'min_g_score':
                        heapq.heappush(open_list, (f_score[new_cell], g_score[new_cell], new_cell))
                    elif tie == 'max_g_score':
                        # print(-g_score[new_cell])
                        # print("lol", new_cell)
                        heapq.heappush(open_list, (f_score[new_cell], -g_score[new_cell], new_cell))

                    path[new_cell] = curr_cell
    # stop_time = timeit.default_timer()
    return None, close_list, h_score


def update_obstacles(cell: tuple, unknown_maze, known_maze):
    n_list = get_neighbors(cell, unknown_maze)
    for neighbor in n_list:
        unknown_maze[neighbor[0]][neighbor[1]] = known_maze[neighbor[0]][neighbor[1]]

    return unknown_maze


def repeated_a_star(unknown_maze: str, known_maze: str, start: tuple, goal: tuple, tie: str, direction: str):
    with open(unknown_maze, 'r') as file:
        unknown_maze = json.load(file)
        unknown_maze = unknown_maze[0]
    #
    # with open(known_maze, 'r') as file:
    #     known_maze = json.load(file)
    #     known_maze = known_maze[0]

    rep_path = {'path_to_goal': [], 'expanded': []}

    initial_cell = start
    goal_cell = goal

    unknown_maze = update_obstacles(start, unknown_maze, known_maze)
    curr_cell = initial_cell
    while curr_cell != goal_cell:
        if direction == 'forwards':
            path = a_star(unknown_maze, curr_cell, goal_cell, tie)
        elif direction == 'backwards':
            path = a_star(unknown_maze, goal_cell, curr_cell, tie)
        rep_path['expanded'].append(path[1])
        path = path[0]

        if path is None:
            return rep_path
        if direction == 'backwards':
            path = path[::-1]

        for step in range(len(path)):
            if is_obstacle(path[step], known_maze):
                curr_cell = path[step - 1]
                rep_path['path_to_goal'].pop()
                unknown_maze = update_obstacles(curr_cell, unknown_maze, known_maze)

                break
            else:
                rep_path['path_to_goal'].append(path[step])
                curr_cell = path[step]
    return rep_path


def adaptive_a_star(unknown, known_maze, start: tuple, goal: tuple):
    h_score = {}

    with open(unknown, 'r') as file:
        unknown_maze = json.load(file)
        unknown_maze = unknown_maze[0]
    #
    # with open(known, 'r') as file:
    #     known_maze = json.load(file)
    #     known_maze = known_maze[0]

    rep_path = {'path_to_goal': [], 'expanded': []}

    unknown_maze = update_obstacles(start, unknown_maze, known_maze)
    curr_cell = start
    while curr_cell != goal:
        path = a_star(unknown_maze, curr_cell, goal, 'max_g_score', h_score)
        rep_path['expanded'].append(path[1])
        h_score = path[2]
        # print(h_score)
        path = path[0]
        if path is None:
            return None
        for step in range(len(path)):
            if is_obstacle(path[step], known_maze):
                curr_cell = path[step - 1]
                rep_path['path_to_goal'].pop()
                unknown_maze = update_obstacles(curr_cell, unknown_maze, known_maze)

                break
            else:
                rep_path['path_to_goal'].append(path[step])
                curr_cell = path[step]

    return rep_path


def is_obstacle(cell, known_maze):
    if known_maze[cell[0]][cell[1]] == 1:
        return True
    else:
        return False


start_cell = (5, 3)
goal_cell = (5, 5)


# Tests for Different a-stars


def part_2(unknown, known, start, goal):
    # Forward A Star with both ties
    t1 = time.time()
    o1 = repeated_a_star(unknown, known, start, goal, tie='min_g_score', direction='forwards')
    e1 = time.time()

    print(f"Repeated Forward A-star (favoring lower g-values): {o1['path_to_goal']}")
    for x in range(len(o1['expanded'])):
        print(f"Iteration {x + 1}: {o1['expanded'][x]}")
        print(f'Num of Cells expanded: {len(o1["expanded"][x])}')

    total = 0
    for x in o1['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")

    print((e1 - t1) * 10 ** 3, "ms")

    print("---------------------")

    t2 = time.time()
    o2 = repeated_a_star("unknown.json", "example_maze.json", start, goal, "h_score", "forwards")

    print(f"Repeated Forward A-star (favoring higher g-values): {o2['path_to_goal']}")
    for x in range(len(o2['expanded'])):
        print(f"Iteration {x + 1}: {o2['expanded'][x]}")
        print(f'Num of Cells expanded: {len(o2["expanded"][x])}')

    total = 0
    for x in o2['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")
    e2 = time.time()
    print((e2 - t2) * 10 ** 3, "ms")


def part_3(unknown, known, start, goal):
    # Comparing A-star forward vs. backward
    t3 = time.time()
    o1 = repeated_a_star(unknown, known, start, goal, 'max_g_score', 'forwards')
    e3 = time.time()

    print(f"Repeated Forward A-star: {o1['path_to_goal']}")
    for x in range(len(o1['expanded'])):
        print(f"Iteration {x + 1}: {o1['expanded'][x]}")
        print(f'Num of Cells expanded: {len(o1["expanded"][x])}')

    total = 0
    for x in o1['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")

    print((e3 - t3) * 10 ** 3, "ms")

    print("---------------------")

    t4 = time.time()

    o1 = repeated_a_star(unknown, known, start, goal, 'max_g_score', 'backwards')
    e4 = time.time()

    print(f"Repeated Backward A-star: {o1['path_to_goal']}")
    for x in range(len(o1['expanded'])):
        print(f"Iteration {x + 1}: {o1['expanded'][x]}")
        print(f'Num of Cells expanded: {len(o1["expanded"][x])}')

    total = 0
    for x in o1['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")

    print((e4 - t4) * 10 ** 3, "ms")


def part_5(unknown, known, start, goal):
    # Repeated Forward vs. Adaptive A-Star
    t3 = time.time()
    o1 = repeated_a_star(unknown, known, start, goal, 'max_g_score', 'forwards')
    e3 = time.time()

    print(f"Repeated Forward A-star: {o1['path_to_goal']}")
    for x in range(len(o1['expanded'])):
        print(f"Iteration {x + 1}: {o1['expanded'][x]}")
        print(f'Num of Cells expanded: {len(o1["expanded"][x])}')

    total = 0
    for x in o1['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")

    print((e3 - t3) * 10 ** 3, "ms")

    print("---------------------")

    t4 = time.time()
    o1 = adaptive_a_star(unknown, known, start, goal)
    e4 = time.time()

    print(f"Adaptive A-star: {o1['path_to_goal']}")
    for x in range(len(o1['expanded'])):
        print(f"Iteration {x + 1}: {o1['expanded'][x]}")
        print(f'Num of Cells expanded: {len(o1["expanded"][x])}')

    total = 0
    for x in o1['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")

    print((e4 - t4) * 10 ** 3, "ms")




