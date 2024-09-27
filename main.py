import random

import a_star
import generate_mazes
import os
import random
import json
import time


# Comparison Tests

def part_2(unknown, known, start, goal):
    # Forward A Star with both ties
    t1 = time.time()
    o1 = a_star.repeated_a_star(unknown, known, start, goal, tie='min_g_score', direction='forwards')
    e1 = time.time()

    print(f"Repeated Forward A-star (favoring lower g-values): {o1['path_to_goal']}")
    # for x in range(len(o1['expanded'])):
    #     print(f"Iteration {x + 1}: {o1['expanded'][x]}")
    #     print(f'Num of Cells expanded: {len(o1["expanded"][x])}')

    total = 0
    for x in o1['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")

    print((e1 - t1) * 10 ** 3, "ms")

    print("---------------------")

    t2 = time.time()
    o2 = a_star.repeated_a_star(unknown, known, start, goal, "max_g_score", "forwards")

    print(f"Repeated Forward A-star (favoring higher g-values): {o2['path_to_goal']}")
    # for x in range(len(o2['expanded'])):
    #     print(f"Iteration {x + 1}: {o2['expanded'][x]}")
    #     print(f'Num of Cells expanded: {len(o2["expanded"][x])}')

    total = 0
    for x in o2['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")
    e2 = time.time()
    print((e2 - t2) * 10 ** 3, "ms")


def part_3(unknown, known, start, goal):
    # Comparing A-star forward vs. backward
    t3 = time.time()
    o1 = a_star.repeated_a_star(unknown, known, start, goal, 'max_g_score', 'forwards')
    e3 = time.time()

    print(f"Repeated Forward A-star: {o1['path_to_goal']}")
    # for x in range(len(o1['expanded'])):
    #     print(f"Iteration {x + 1}: {o1['expanded'][x]}")
    #     print(f'Num of Cells expanded: {len(o1["expanded"][x])}')

    total = 0
    for x in o1['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")

    print((e3 - t3) * 10 ** 3, "ms")

    print("---------------------")

    t4 = time.time()

    o1 = a_star.repeated_a_star(unknown, known, start, goal, 'max_g_score', 'backwards')
    e4 = time.time()

    print(f"Repeated Backward A-star: {o1['path_to_goal']}")
    # for x in range(len(o1['expanded'])):
    #     print(f"Iteration {x + 1}: {o1['expanded'][x]}")
    #     print(f'Num of Cells expanded: {len(o1["expanded"][x])}')

    total = 0
    for x in o1['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")

    print((e4 - t4) * 10 ** 3, "ms")


def part_5(unknown, known, start, goal):
    # Repeated Forward vs. Adaptive A-Star
    t3 = time.time()
    o1 = a_star.repeated_a_star(unknown, known, start, goal, 'max_g_score', 'forwards')
    e3 = time.time()

    print(f"Repeated Forward A-star: {o1['path_to_goal']}")
    # for x in range(len(o1['expanded'])):
    #     print(f"Iteration {x + 1}: {o1['expanded'][x]}")
    #     print(f'Num of Cells expanded: {len(o1["expanded"][x])}')

    total = 0
    for x in o1['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")

    print((e3 - t3) * 10 ** 3, "ms")

    print("---------------------")

    t4 = time.time()
    o1 = a_star.adaptive_a_star(unknown, known, start, goal)
    e4 = time.time()

    print(f"Adaptive A-star: {o1['path_to_goal']}")
    # for x in range(len(o1['expanded'])):
    #     print(f"Iteration {x + 1}: {o1['expanded'][x]}")
    #     print(f'Num of Cells expanded: {len(o1["expanded"][x])}')

    total = 0
    for x in o1['expanded']:
        total += len(x)

    print(f"Total cells expanded: {total}")

    print((e4 - t4) * 10 ** 3, "ms")


if __name__ == "__main__":

    if not os.path.isfile('./grids.json'):
        generate_mazes.generate()

    rand_grid_num = random.randint(0, 49)

    with open('grids.json', 'r') as file:
        rand_grid = json.load(file)
        rand_grid = rand_grid[rand_grid_num]

    rand_start = random.randint(1, 101), random.randint(1, 101)
    rand_goal = random.randint(1, 101), random.randint(1, 101)

    while rand_grid[rand_start[0]][rand_start[1]] == 1:
        rand_start = random.randint(1, 101), random.randint(1, 101)
    while rand_grid[rand_goal[0]][rand_goal[1]] == 1:
        rand_goal = random.randint(1, 101), random.randint(1, 101)

    print("Comparing Repeated Forward A-Star with both ties")
    part_2(unknown="empty_maze.json", known=rand_grid, start=rand_start, goal=rand_goal)

    print("=============================="
          "=============================="
          "==============================")

    print("Comparing Repeated Forward vs. Backward A-Star")
    part_3(unknown="empty_maze.json", known=rand_grid, start=rand_start, goal=rand_goal)

    print("=============================="
          "=============================="
          "==============================")

    print("Comparing Adaptive vs Repeated Forward A-Star")
    part_5(unknown="empty_maze.json", known=rand_grid, start=rand_start, goal=rand_goal)
