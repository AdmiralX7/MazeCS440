import random
import comparisons
import generate_mazes
import maze_display
import os
import json

if __name__ == "__main__":

    if not os.path.isfile('./grids.json'):
        print("Generating Mazes")
        generate_mazes.generate()

    with open('grids.json', 'r') as file:
        grids = json.load(file)

    print("Running comparisons...")

    path_data = comparisons.run_comparisons(grids)

    while True:
        visualize = str(input("Visualize a Random Grid? Y/N: "))
        if visualize.lower() == "y":
            astar_type = int(input(
                                   "Repeated Forward (ties favoring greater g-score) [0]\n"
                                   "Repeated Forward A* (ties favoring lower g-score) [1]\n"
                                   "Repeated Backward A* [2]\n"
                                   "Adaptive A* [3] \n"
                                   "Enter A* type: "
            ))
            random_grid_num = random.randint(0, 49)
            if astar_type == 0:
                maze_display.display_path(grids[random_grid_num],
                                          path_data['forwards_astar_max'][random_grid_num]['path_to_goal'])
            elif astar_type == 1:
                maze_display.display_path(grids[random_grid_num],
                                          path_data['forwards_astar_min'][random_grid_num]['path_to_goal'])
            elif astar_type == 2:
                maze_display.display_path(grids[random_grid_num],
                                          path_data['backwards_astar'][random_grid_num]['path_to_goal'])
            elif astar_type == 3:
                maze_display.display_path(grids[random_grid_num],
                                          path_data['adaptive_astar'][random_grid_num]['path_to_goal'])
        elif visualize.lower() == 'n':
            break
