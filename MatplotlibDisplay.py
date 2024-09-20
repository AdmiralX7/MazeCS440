import numpy as np
import matplotlib.pyplot as plt
import time

# Generate a 10x10 random maze with 1's as walls and 0's as paths
maze = np.random.randint(2, size=(100, 100))

# Set a start and end point
start = (0, 0)
end = (9, 9)
maze[start] = 0  # Ensure the start is a path
maze[end] = 0    # Ensure the end is a path

# Create a separate array to track the runner's path
trail_maze = np.full(maze.shape, 2)  # Initialize with a value that won't affect display

# Function to display the maze with the runner's position and trail
def display_maze(maze, trail_maze, runner_position):
    plt.clf()  # Clear the previous plot
    display_array = np.where(trail_maze == 0, 0.5, maze)  # Show trail as gray
    plt.imshow(display_array, cmap='gray', interpolation='none')
    plt.scatter(runner_position[1], runner_position[0], c='red', s=100)  # Mark the runner
    plt.draw()  # Draw the updated plot
    plt.pause(0.1)  # Pause to update the display

# Initialize the runner's position
runner_position = list(start)

# Display the initial state of the maze
plt.ion()  # Turn on interactive mode
fig = plt.figure()

# Simulate the runner moving through the maze and leaving a trail
movements = [(0, 1), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3)]

for move in movements:
    trail_maze[runner_position[0], runner_position[1]] = 0  # Mark the trail
    runner_position = move
    display_maze(maze, trail_maze, runner_position)
    time.sleep(0.5)  # Pause to simulate the runner's movement

plt.ioff()  # Turn off interactive mode
plt.show()
