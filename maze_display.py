import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def display_path(maze, path):  # path is a list of tuples
    plt.ion()

    maze_array = maze
    cmap = mcolors.ListedColormap(['white', 'black', 'green', 'red', 'blue'])

    if len(path) == 0:
        print("Impossible to reach goal")
        return

    maze_array[path[0][0]][path[0][1]] = 2
    maze_array[path[-1][0]][path[-1][1]] = 3
    path = path[1:-1]
    for cell in path:
        plt.clf()
        if maze[cell[0]][cell[1]] != 2:
            maze[cell[0]][cell[1]] = 4
        plt.imshow(maze, cmap=cmap, interpolation='none')
        plt.draw()
        plt.pause(0.1)

    plt.imshow(maze, cmap=cmap, interpolation='none')

    plt.ioff()
    plt.show()


def display_maze(maze):

    plt.ion()
    cmap = mcolors.ListedColormap(['white', 'black'])
    plt.imshow(maze, cmap=cmap, interpolation='none')
    plt.ioff()
    plt.show()
