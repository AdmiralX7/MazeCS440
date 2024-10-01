import time
import a_star
import random


def comp_repeated_a_star(unknown, known, start, goal, tie, direction):
    t1 = time.time()
    o1 = a_star.repeated_a_star(unknown, known, start, goal, tie=tie, direction=direction)
    e1 = time.time()

    total = 0
    for x in o1['expanded']:
        total += len(x)

    run_time = (e1 - t1) * 10 ** 3

    return total, run_time, o1


def comp_adaptive_a_star(unknown, known, start, goal):
    t1 = time.time()
    o1 = a_star.adaptive_a_star(unknown, known, start, goal)
    e1 = time.time()

    total = 0
    for x in o1['expanded']:
        total += len(x)

    run_time = (e1 - t1) * 10 ** 3

    return total, run_time, o1


def run_comparisons(mazes):
    # Runs comparisons of all A*'s

    total_forwards_astar_min_time = 0
    total_forwards_astar_max_time = 0
    total_backwards_astar_time = 0
    total_adaptive_astar_time = 0
    total_forwards_astar_min_cells = 0
    total_forwards_astar_max_cells = 0
    total_backwards_astar_cells = 0
    total_adaptive_astar_cells = 0
    grid_count = 0

    path_data = {'forwards_astar_min': [], 'forwards_astar_max': [], 'backwards_astar': [], 'adaptive_astar': []}

    for grid in mazes:

        rand_start = random.randint(0, 100), random.randint(0, 100)
        rand_goal = random.randint(0, 100), random.randint(0, 100)

        while grid[rand_start[0]][rand_start[1]] == 1:
            rand_start = random.randint(0, 100), random.randint(0, 100)
        while grid[rand_goal[0]][rand_goal[1]] == 1:
            rand_goal = random.randint(0, 100), random.randint(0, 100)
        forwards_astar_min = comp_repeated_a_star("empty_maze.json", grid, rand_start, rand_goal, 'min_g_score',
                                                  'forwards')
        forwards_astar_max = comp_repeated_a_star("empty_maze.json", grid, rand_start, rand_goal, 'max_g_score',
                                                  'forwards')
        backwards_astar = comp_repeated_a_star("empty_maze.json", grid, rand_start, rand_goal, 'max_g_score',
                                               'backwards')
        adaptive_astar = comp_adaptive_a_star("empty_maze.json", grid, rand_start, rand_goal)

        path_data['forwards_astar_min'].append(forwards_astar_min[2])
        path_data['forwards_astar_max'].append(forwards_astar_max[2])
        path_data['backwards_astar'].append(backwards_astar[2])
        path_data['adaptive_astar'].append(adaptive_astar[2])

        grid_count += 1
        print(f"{grid_count}: 50 grids")
        total_forwards_astar_min_time += forwards_astar_min[1]
        total_forwards_astar_min_cells += forwards_astar_min[0]
        total_forwards_astar_max_time += forwards_astar_max[1]
        total_forwards_astar_max_cells += forwards_astar_max[0]

        total_backwards_astar_time += backwards_astar[1]
        total_backwards_astar_cells += backwards_astar[0]
        total_adaptive_astar_time += adaptive_astar[1]
        total_adaptive_astar_cells += adaptive_astar[0]

    print("=====================================")
    print("Average values")
    print("=====================================")
    print("Repeated Forward A* (ties favoring lower g-scores)")
    print("Run time: ", round(total_forwards_astar_min_time / 50, 3), "ms")
    print("Cells Explored: ", round(total_forwards_astar_min_cells / 50, 3))
    print("=====================================")
    print("Repeated Forward A* (ties favoring higher g-scores)")
    print("Run time: ", round(total_forwards_astar_max_time / 50, 3), "ms")
    print("Cells Explored: ", round(total_forwards_astar_max_cells / 50, 3))
    print("=====================================")
    print("Repeated Forward A*")
    print("Run time: ", round(total_forwards_astar_max_time / 50, 3), "ms")
    print("Cells Explored: ", round(total_forwards_astar_max_cells / 50, 3))
    print("=====================================")
    print("Repeated Backward A*")
    print("Run time: ", round(total_backwards_astar_time / 50, 3), "ms")
    print("Cells Explored: ", round(total_backwards_astar_cells / 50, 3))
    print("=====================================")
    print("Adaptive A*")
    print("Run time: ", round(total_adaptive_astar_time / 50, 3), "ms")
    print("Cells Explored: ", round(total_adaptive_astar_cells / 50, 3))

    return path_data
