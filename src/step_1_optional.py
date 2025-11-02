import sys
import json
import os

# CONFIGURACIÓN DE ARCHIVOS
file_name = input("Enter the name of the input file (for example, dom07):")
output_file = file_name 
file_name = file_name + ".txt"
output_file = output_file + ".json"

in_path = os.path.join(".", "examplesthermo_curved", file_name)
output_dir = os.path.join(".", "examplesthermo_curved")

out_path = os.path.join(output_dir, output_file)

# SYMBOLS
ARROWS = {'^': (-1, 0), 'v': (1, 0), '>': (0, 1), '<': (0, -1)}

# Bulbs (initial direction)
BULBS  = {'U': (-1, 0), 'D': (1, 0), 'R': (0, 1), 'L': (0, -1)}

# Turns (curves) as in the statement: 0,1,2,3 = └ ┏ ┐ ┘  (rotations)
# Map: (entry_dir) -> (exit_dir)
# Convention: Up=(-1,0), Down=(1,0), Right=(0,1), Left=(0,-1)
CORNER_TURNS = {
    '0': { (1,0):(0,1),  (0,-1):(-1,0) },   # └ : from Down to Right, from Left to Up
    '1': { (-1,0):(0,1), (0,-1):(1,0) },    # ┏ : from Up to Right,  from Left to Down
    '2': { (-1,0):(0,-1),(0,1):(1,0) },     # ┐ : from Up to Left,   from Right to Down
    '3': { (1,0):(0,-1), (0,1):(-1,0) }     # ┘ : from Down to Left, from Right to Up
}

def in_bounds(n, r, c):  # Check whether a position (r, c) is within the bounds of the n×n grid.
    return 0 <= r < n and 0 <= c < n

def read_instance(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    if len(lines) < 3:
        print("Error: the input is too short.")
        sys.exit(1)

    col_line = lines[-2].strip()
    row_line = lines[-1].strip()
    
    try:
        col_sums = [int(x) for x in col_line.split()]
        row_sums = [int(x) for x in row_line.split()]
    except ValueError:
        print("Error: the last two lines must contain space-separated integers.")
        sys.exit(1)

    n = len(col_sums)
    assert n == len(row_sums), "Row/column sums with different sizes"

    grid_lines = lines[:-2]
    assert len(grid_lines) == n, f"Expected {n} grid rows but got {len(grid_lines)}"
    
    grid = [list(row) for row in grid_lines]
    for r in range(n):
        assert len(grid[r]) == n, f"Row {r} does not have {n} columns"
    return grid, col_sums, row_sums

def from_bulb_curved(grid, r, c, dr, dc):
    """
    Follow the thermometer from (r, c) in direction (dr, dc):
    - If it finds a straight segment, continue straight (symbol consistent with the direction).
    - If it finds a turn 0/1/2/3, change direction according to CORNER_TURNS.
    - Stop when it can no longer move forward (out of bounds or incompatible symbol).
    Returns a list of cells [(r0, c0), (r1, c1), ...], starting from the bulb.
    """
    n = len(grid)
    path = [(r, c)]
    
    direct = {(-1,0):'^', (1,0):'v', (0,1):'>', (0,-1):'<'}
    rr, cc = r + dr, c + dc
    cur_dr, cur_dc = dr, dc

    while in_bounds(n, rr, cc):
        ch = grid[rr][cc]

        if ch in ARROWS:
         # must match the current direction
            if ch != direct[(cur_dr, cur_dc)]:
                break
            path.append((rr, cc))
            rr += cur_dr
            cc += cur_dc
            continue

        elif ch in CORNER_TURNS:
            turn_map = CORNER_TURNS[ch]

            # the *entry* direction to the cell is the current movement direction
            entry_dir = (cur_dr, cur_dc)

            if entry_dir not in turn_map:
            # Incompatible curve: the thermometer ends before this cell
                break

            path.append((rr, cc))
            cur_dr, cur_dc = turn_map[entry_dir]  # new direction after the turn
            rr += cur_dr
            cc += cur_dc
            continue

        else:
            break

    return path

def build_thermos(grid):
    """
    Find bulbs and build paths (with possible turns).
    Validate:
      1) No overlaps.
      2) Every symbolic cell (bulb/straight/turn) belongs to some path.
    """
    n = len(grid)
    bulbs = []
    thermo_paths = []
    used = set()

    # find bulbs
    for r in range(n):
        for c in range(n):
            ch = grid[r][c]
            if ch in BULBS:
                bulbs.append((r, c, *BULBS[ch]))

    # follow each bulb
    for (r, c, dr, dc) in bulbs:
        path = from_bulb_curved(grid, r, c, dr, dc)

        for (pr, pc) in path:
            if (pr, pc) in used:
                raise AssertionError(f"Overlap: cell {pr},{pc} belongs to >1 thermometer")
            used.add((pr, pc))
        thermo_paths.append(path)

    # Validation: any grid symbol related to thermometers
    # must be in some path (bulbs, straights, turns)
    for r in range(n):
        for c in range(n):
            ch = grid[r][c]
            if ch in BULBS or ch in ARROWS or ch in CORNER_TURNS:
                if (r, c) not in used:
                    print(f"Error: cell {r},{c} with symbol '{ch}' not connected to any bulb.")
                    sys.exit(1)
                    
    return bulbs, thermo_paths

def main():
    grid, col_sums, row_sums = read_instance(in_path)

    bulbs, thermo_paths = build_thermos(grid)

    # JSON Format
    n = len(grid)
    bulbs_json = [{"r": r, "c": c, "dr": dr, "dc": dc} for (r, c, dr, dc) in bulbs]
    thermos_json = [[{"r": rr, "c": cc} for (rr, cc) in path] for path in thermo_paths]

    obj = {
        "n": n,
        "grid": grid,
        "bulbs": bulbs_json,
        "thermometers": thermos_json,
        "row_targets": row_sums,
        "col_targets": col_sums
    }
    # Save JSON file
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

    print("Conversion completed successfully.")
    print(f"JSON file saved to: {out_path}")
    print(f"Grid size: {n}x{n}")
    print(f"{len(thermos_json)} thermometers detected.")

if __name__ == "__main__":
    main()
