import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import random
import json
import time

# ------------------ FUNCTIONS ------------------
def mazeArray(receivedGrid):
    # Create an array of 1's and 0's from the grid
    gridArray = []
    for row in receivedGrid:
        newRow = []
        for cell in row:
            if cell['blocked']:
                newRow.append(1)
            else:
                newRow.append(0)
        gridArray.append(newRow)

    return gridArray

"""def displayMaze(receivedArray):

    # Convert gridArray to a numpy array for imshow
    npArray = np.array(receivedArray)
    
    # Save the grid array to a text file
    np.savetxt('mazeGrid.txt', npArray, fmt='%d')

    # Define a custom colormap: white for 0 and black for 1
    cmap = mcolors.ListedColormap(['white', 'black'])

    # Display the maze
    plt.imshow(npArray, cmap=cmap, interpolation='none')
    plt.title('Maze Visualization')
    plt.show()
"""

# Function to display the maze with the runner's position and trail
def displayMaze(maze, trail_maze, runner_position):
    plt.clf()  # Clear the previous plot
    display_array = np.where(trail_maze == 0, 0.5, maze)  # Show trail as gray

    # Create a custom colormap: white for 0 and black for 1
    cmap = mcolors.ListedColormap(['white', 'gray', 'black'])

    plt.imshow(display_array, cmap=cmap, interpolation='none')
    plt.scatter(runner_position[1], runner_position[0], c='red', s=100)  # Mark the runner
    plt.draw()  # Draw the updated plot
    plt.pause(0.1)  # Pause to update the display

# Function to load grids from a JSON file
def loadGrids(maze):    
    # Convert back to grid format if needed
    grid = []
    for row in maze:
        newRow = [{'blocked': bool(cell), 'visited': False} for cell in row]
        grid.append(newRow)
    
    return grid

def display(maze, path):

    maze_array = np.array(maze)  # Convert the list to a NumPy array
    loadedGrid = loadGrids(maze_array)


    # Create a separate array to track the runner's path
    trail_maze = np.full(maze_array.shape, 2)  # Use the shape of the NumPy array

    # Display the initial state of the maze
    plt.ion()  # Turn on interactive mode
    fig = plt.figure()

    runner_position = path[0]  # Initialize the runner's position

    for move in path:
        trail_maze[runner_position[0], runner_position[1]] = 0  # Mark the trail
        runner_position = move
        displayMaze(maze, trail_maze, runner_position)
        time.sleep(0.5)  # Pause to simulate the runner's movement

    plt.ioff()  # Turn off interactive mode
    plt.show()

    output_file = 'output.txt'

    # Open the file in append mode
    with open(output_file, 'a') as f:
        print("Checking maze.", file=f)
        print(loadedGrid, file=f)

        print("Checking path.", file=f)
        print(path, file=f)

