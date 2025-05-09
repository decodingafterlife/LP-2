import random
import copy

GRID_SIZE = 9
BOX_SIZE = 3

def print_grid(grid):
    for row in grid:
        print(" ".join(str(num) if num != 0 else '.' for num in row))

def get_conflicts(grid):
    conflicts = 0
    # Column conflicts
    for col in range(GRID_SIZE):
        col_vals = [grid[row][col] for row in range(GRID_SIZE)]
        conflicts += GRID_SIZE - len(set(col_vals))
    
    # Box conflicts
    for box_row in range(0, GRID_SIZE, BOX_SIZE):
        for box_col in range(0, GRID_SIZE, BOX_SIZE):
            box = []
            for i in range(BOX_SIZE):
                for j in range(BOX_SIZE):
                    box.append(grid[box_row + i][box_col + j])
            conflicts += GRID_SIZE - len(set(box))
    return conflicts

def fill_grid(grid, fixed):
    # Fill each row with digits 1–9, maintaining fixed cells
    new_grid = copy.deepcopy(grid)
    for i in range(GRID_SIZE):
        missing = [x for x in range(1, 10) if x not in new_grid[i]]
        random.shuffle(missing)
        for j in range(GRID_SIZE):
            if not fixed[i][j]:
                new_grid[i][j] = missing.pop()
    return new_grid

def get_neighbors(grid, fixed):
    neighbors = []
    for i in range(GRID_SIZE):
        # Only consider non-fixed positions
        indices = [j for j in range(GRID_SIZE) if not fixed[i][j]]
        for a in range(len(indices)):
            for b in range(a+1, len(indices)):
                new_grid = copy.deepcopy(grid)
                j1, j2 = indices[a], indices[b]
                # Swap two elements in the same row
                new_grid[i][j1], new_grid[i][j2] = new_grid[i][j2], new_grid[i][j1]
                neighbors.append(new_grid)
    return neighbors

def hill_climb(grid):
    fixed = [[cell != 0 for cell in row] for row in grid]
    current = fill_grid(grid, fixed)
    current_score = get_conflicts(current)

    while True:
        neighbors = get_neighbors(current, fixed)
        next_grid = None
        next_score = current_score

        for neighbor in neighbors:
            score = get_conflicts(neighbor)
            if score < next_score:
                next_grid = neighbor
                next_score = score
        
        if next_score >= current_score:
            break  # Local optimum reached
        current = next_grid
        current_score = next_score
    return current, current_score

# Example Sudoku Puzzle
initial_grid = [
    [5, 1, 7, 6, 0, 0, 0, 3, 4],
    [2, 8, 9, 0, 0, 4, 0, 0, 0],
    [3, 4, 6, 2, 0, 5, 0, 9, 0],
    [6, 0, 2, 0, 0, 0, 0, 1, 0],
    [0, 3, 8, 0, 0, 6, 0, 4, 7],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 9, 0, 0, 0, 0, 0, 7, 8],
    [7, 0, 3, 4, 0, 0, 5, 6, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

solution, score = hill_climb(initial_grid)
print("Final Sudoku Grid with Conflicts:", score)
print_grid(solution)
