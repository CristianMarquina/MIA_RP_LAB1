# Step 1 objective:
#     Read the ASCII files (e.g., dom01.txt)
#     Define the meaning of characters
#     Specify the structure of the input file

import os
import json
import sys

file_name = input("Enter the name of the input file (for example, dom01): ")
output_file = file_name 
file_name = file_name + ".txt"
output_file = output_file + ".json"

in_path = os.path.join(".", "examplesthermo", file_name)
output_dir = os.path.join(".", "examplesthermo")

out_path = os.path.join(output_dir, output_file)

symbols = {"^" : (-1,0), "v" : (1,0), "<" : (0,-1), ">" : (0,1)}
bulbs = {"U" : (-1,0), "D" : (1,0), "L" : (0,-1), "R" : (0,1)}

def in_bounds(n, r, c):   # Check whether rows and columns are within n
    if r < 0 or r >= n:  # Verify whether the row (r) is within n (size)
        return False
    
    if c < 0 or c >= n:
        return False
    
    return True

def read_instance(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = []
        for line in f:
            lines.append(line.strip())

    #  The last two lines contain the numbers associated to columns (first line) and rows (second line) separated by blank spaces. 
    col_line = lines[-2].strip()      
    row_line = lines[-1].strip()

    # We need to convert these values into integers
    col_sum = []
    for i in col_line.split():
        col_sum.append(int(i))

    row_sum = []
    for i in row_line.split():
        row_sum.append(int(i))

    # Size is n x n
    n = len(col_sum)
    assert n == len(row_sum), "Row/column sums with different sizes"
    
    # We get the grid we are interested in
    grid_lines = lines[:-2]
    assert len(grid_lines) == n, f"Expected {n} grid rows but got {len(grid_lines)}"
    
    grid = []
    for row in grid_lines:
        grid.append(list(row))

    # Check that each row has the correct number of columns
    for i in range(n):
        if len(grid[i]) != n:
            print(f"Error: row {i} does not have {n} columns")
            return None

    return grid, col_sum, row_sum


def from_bulbs(grid, r, c, rd, cd): #rd: row direction, cd: column direction
    n = len(grid)
    path = [(r, c)]

    if rd == -1 and cd == 0: seg = '^'
    elif rd == 1 and cd == 0: seg = 'v'    
    elif rd == 0 and cd == 1: seg = '>'  
    elif rd == 0 and cd == -1: seg = '<'   
    else:
        print("Error: invalid bulb direction.")
        return None
    
    # Calculate the new position
    rr = r + rd
    cc = c + cd
    while in_bounds(n, rr, cc) and grid[rr][cc] == seg: # while we are within the bounds and the symbol is correct
        path.append((rr, cc))
        # Update the position // move in the direction of the bulb
        rr += rd
        cc += cd

    return path


def thermos(grid):  # Find bulbs, build complete paths, and validate that they neither cross nor change direction.

    n = len(grid)

    found_bulbs = []
    thermo_paths = []   
    used = set()  # Set of already-used cells (to detect overlaps)
    
    # find bulbos
    for r in range(n):
        for c in range(n):
            ch = grid[r][c]
            if ch in bulbs:
                rd, cd = bulbs[ch]
                if (r, c) in used:
                    continue

                path = from_bulbs(grid, r, c, rd, cd) # Get the path from the bulb
                # Check for overlaps
                for (row, col) in path:
                    if (row, col) in used:
                        print("Error: thermos paths overlap at cell", (row, col))
                        return None
                    used.add((row, col)) # Add the cell to the set of used ones
                found_bulbs.append((r, c, rd, cd))
                thermo_paths.append(path)

        # Verify that there are no blank cells
    for r in range(n):
        for c in range(n):
            ch = grid[r][c]
            if ch in bulbs or ch in symbols:
                if (r, c) not in used:
                    print(f"Error: cell {r},{c} with symbol '{ch}' not connected to any bulb")
                    return None
                    
    return found_bulbs, thermo_paths  

def main():
    instance_data = read_instance(in_path)
    if instance_data is None:
        print("Error reading instance file. Exiting.")
        return
    grid, col_sums, row_sums = instance_data

    thermos_data = thermos(grid)
    if thermos_data is None:
        print("Error processing thermometers. Exiting.")
        return
    found_bulbs, thermo_paths = thermos_data

    # formato json
    n = len(grid)
    bulbs_json = []
    for (r, c, dr, dc) in found_bulbs:
        bulbs_json.append({"r": r, "c": c, "dr": dr, "dc": dc})

    thermos_json = []
    for path in thermo_paths:
        one_thermo = []
        for (r, c) in path: 
            one_thermo.append({"r": r, "c": c})
        thermos_json.append(one_thermo)

    data = {
        "n": n,
        "grid": grid,
        "bulbs": bulbs_json,
        "thermometers": thermos_json,
        "row_targets": row_sums,
        "col_targets": col_sums}
    
    #guardan archivo json
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Converion succeeded.")
    print(f"json file saved in {out_path}")
    print(f"Size of the grid: {n}x{n}")
    print(f"There are {len(thermos_json)} termometers.")

if __name__ == "__main__":
    main()