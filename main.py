import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import random
import json
import time

# ------------------ FUNCTIONS ------------------
def chooseRandomCell():
    unvisitedCells = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if not grid[x][y]['visited'] and not grid[x][y]['blocked']:
                unvisitedCells.append((x, y))

    if not unvisitedCells:
        return None  # No more unvisited cells
    
    return random.choice(unvisitedCells)

def getNeighbors(x, y):
    neighbors = []

    # Check the North neighbor
    if not grid[x - 1][y]['visited'] and not grid[x - 1][y]['blocked']:
        neighbors.append((x - 1, y))

    # Check the South neighbor
    if not grid[x + 1][y]['visited'] and not grid[x + 1][y]['blocked']:
        neighbors.append((x + 1, y))

    # Check the West neighbor
    if not grid[x][y - 1]['visited'] and not grid[x][y - 1]['blocked']:
        neighbors.append((x, y - 1))

    # Check the East neighbor
    if not grid[x][y + 1]['visited'] and not grid[x][y + 1]['blocked']:
        neighbors.append((x, y + 1))

    return neighbors

def blockProbability(x, y):
    if random.random() < 0.3:  # 30% probability
        grid[x][y]['blocked'] = True
        return True
    else:  # 70% probability
        grid[x][y]['blocked'] = False
        return False


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

def displayMaze(receivedArray):

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

def saveGridsToJson(receivedGrid, filename='grids.json'):
    gridsList = []
    
    for grid in receivedGrid:
        gridArray = []
        for row in grid:
            newRow = []
            for cell in row:
                newRow.append(1 if cell['blocked'] else 0)
            gridArray.append(newRow)
        gridsList.append(gridArray)
    
    with open(filename, 'w') as f:
        json.dump(gridsList, f)

# Function to load grids from a JSON file
def loadGridsFromJson(filename='grids.json'):
    with open(filename, 'r') as f:
        gridsList = json.load(f)
    
    # Convert back to grid format if needed
    grids = []
    for gridArray in gridsList:
        grid = []
        for row in gridArray:
            newRow = [{'blocked': bool(cell), 'visited': False} for cell in row]
            grid.append(newRow)
        grids.append(grid)
    
    return grids

# --------------------- MAIN ---------------------
if __name__ == '__main__':
    # Start the timer
    startTime = time.time()

    allGrid = []

    # Simulate saving 50 grids
    for i in range(50):
        # --------------- MAP Initialization ---------------
        
        gridSize = 101
        # Initialize an empty grid list
        grid = []

        # Create each row and add to the grid
        for i in range(gridSize):
            row = []
            for j in range(gridSize):
                # Append a dictionary to the row
                row.append({'visited': False, 'blocked': False})
            
            # Append the row to the grid
            grid.append(row)

        # Add blocked boundaries around the edges
        for i in range(gridSize):
            grid[0][i]['blocked'] = True   # Top boundary
            grid[gridSize-1][i]['blocked'] = True   # Bottom boundary
            grid[i][0]['blocked'] = True   # Left boundary
            grid[i][gridSize-1]['blocked'] = True   # Right boundary

        # Stack to manage the DFS traversal
        stack = []

        # Simulate the runner moving through the maze
        movements = []

        while True:
            # If the stack is empty, choose a new random starting position
            if not stack:
                # Choose a random starting point within the grid
                initialCell = chooseRandomCell()

                if not initialCell:
                    
                    print("All cells have been visited. Exiting the code.")
                    break  # Exit the loop and terminate the program

                InitialX, InitialY = initialCell

                stack.append((InitialX, InitialY))
                movements.append((InitialX, InitialY))

                # Mark the start cell as visited
                grid[InitialX][InitialY]['visited'] = True
                # print(f"New starting point chosen: ({InitialX}, {InitialY})")

            # Current position is the last position in the stack
            currentX, currentY = stack[-1]

            possibleMoves = getNeighbors(currentX, currentY)
            
            if not possibleMoves:
                # No more moves from this position, backtrack
                stack.pop()
            else:
                # Randomly choose a neighbor to move to
                nextMove = random.choice(possibleMoves)
                # print("Attempting to move to:", nextMove)

                if blockProbability(nextMove[0], nextMove[1]):
                    # print("Blocked cell encountered:", nextMove)
                    grid[nextMove[0]][nextMove[1]]['visited'] = True
                    grid[nextMove[0]][nextMove[1]]['blocked'] = True
                    possibleMoves.remove(nextMove)
                    movements.append(nextMove)
                    movements.append((currentX,currentY))
                    
                else:
                    # print("Moving to:", nextMove)
                    stack.append(nextMove)
                    movements.append(nextMove)
                    grid[nextMove[0]][nextMove[1]]['visited'] = True

        allGrid.append(grid)
    """
        grid = mazeArray(grid)
        displayMaze(grid)
    """

    saveGridsToJson(allGrid)
    loadedGrids = loadGridsFromJson()

    # Stop the timer
    endTime = time.time()

    # Calculate and print the total time taken
    totalTime = endTime - startTime
    print(f"Total time taken: {totalTime:.2f} seconds")

    # To access a specific grid, say the first one:
    firstGrid = loadedGrids[0]
    firstGrid = mazeArray(firstGrid)
    displayMaze(firstGrid)