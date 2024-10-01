import random
import json


def choose_random_cell(grid):
    unvisitedCells = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if not grid[x][y]['visited'] and not grid[x][y]['blocked']:
                unvisitedCells.append((x, y))

    if not unvisitedCells:
        return None

    return random.choice(unvisitedCells)


def get_neighbors(grid, x, y):
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


def save_grids_to_json(received_grid, filename='grids.json'):
    gridsList = []

    for grid in received_grid:
        gridArray = []
        for row in grid:
            newRow = []
            for cell in row:
                newRow.append(1 if cell['blocked'] else 0)
            gridArray.append(newRow)
        gridsList.append(gridArray)

    with open(filename, 'w') as f:
        json.dump(gridsList, f)


def block_probability(grid, x, y):
    if random.random() < 0.3:
        grid[x][y]['blocked'] = True
        return True
    else:
        grid[x][y]['blocked'] = False
        return False


def generate():
    all_grid = []
    for x in range(50):
        grid_size = 101 + 2
        grid = []

        for y in range(grid_size):
            row = []
            for j in range(grid_size):
                row.append({'visited': False, 'blocked': False})

            grid.append(row)

        for i in range(grid_size):
            grid[0][i]['blocked'] = True  # Top boundary
            grid[grid_size - 1][i]['blocked'] = True  # Bottom boundary
            grid[i][0]['blocked'] = True  # Left boundary
            grid[i][grid_size - 1]['blocked'] = True  # Right boundary

        stack = []

        movements = []

        while True:
            # If the stack is empty, choose a new random starting position
            if not stack:
                # Choose a random starting point within the grid
                initialCell = choose_random_cell(grid)

                if not initialCell:
                    print("All cells have been visited. Exiting the code.")
                    break

                InitialX, InitialY = initialCell

                stack.append((InitialX, InitialY))
                movements.append((InitialX, InitialY))

                grid[InitialX][InitialY]['visited'] = True
                # print(f"New starting point chosen: ({InitialX}, {InitialY})")

            # Current position is the last position in the stack
            currentX, currentY = stack[-1]

            possibleMoves = get_neighbors(grid, currentX, currentY)

            if not possibleMoves:
                stack.pop()
            else:
                nextMove = random.choice(possibleMoves)
                # print("Attempting to move to:", nextMove)

                if block_probability(grid, nextMove[0], nextMove[1]):
                    # print("Blocked cell encountered:", nextMove)
                    grid[nextMove[0]][nextMove[1]]['visited'] = True
                    grid[nextMove[0]][nextMove[1]]['blocked'] = True
                    possibleMoves.remove(nextMove)
                    movements.append(nextMove)
                    movements.append((currentX, currentY))

                else:
                    # print("Moving to:", nextMove)
                    stack.append(nextMove)
                    movements.append(nextMove)
                    grid[nextMove[0]][nextMove[1]]['visited'] = True

        all_grid.append(grid)
        save_grids_to_json(all_grid)
