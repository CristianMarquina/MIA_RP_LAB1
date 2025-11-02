import os
import json
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python src/encode.py examplesthermo/dom__.json facts/domain__.lp")
        sys.exit(1)
    json_file = sys.argv[1]
    out_lp = sys.argv[2]
    output_dir = os.path.join(".", "facts")
    os.makedirs(output_dir, exist_ok=True)

    with open(json_file, "r", encoding="utf-8") as f: 
        data = json.load(f)

    n = data["n"]  # size of the grid
    grid = data["grid"] 
    bulbs = data["bulbs"]  # [{"r", "c", "dr", "dc"}, {...}, ...]
    thermos = data["thermometers"]  #[{"r", "c"}, º{...}, ...]
    row_targets = data["row_targets"]  # int list
    col_targets = data["col_targets"]  # int list

    facts = []
    facts.append(f"dim({n}).")

    # cell/2. find every cell that is part of any thermometer (bulb or part)
    cells = set()
    for path in thermos: 
        for node in path: 
            cells.add( (node["r"], node["c"]) )
    for (r,c) in sorted(cells):  #funcionaria igual si no estuviera el sorted, es solo para ordenar la salida (legibilidad)
        facts.append(f"cell({r},{c}).")
            
    # bulb/2. find every bulb
    for bulb in bulbs:
        facts.append(f"bulb({bulb['r']},{bulb['c']}).")

    # prev/4: find every father-son relation in thermometers
    for path in thermos:
        for i in range(1, len(path)):
            r = path[i]["r"]
            c = path[i]["c"]
            pr = path[i-1]["r"]
            pc = path[i-1]["c"]
            facts.append(f"prev({r},{c},{pr},{pc}).")
            # If the path is (b0) -> (b1) -> (b2), we would generate: prev(b1,b0) and prev(b2,b1).
    
    # targets de columnas y filas
    for c, k in enumerate(col_targets, start=0):
        facts.append(f"col_target({c},{k}).")
    for r, k in enumerate(row_targets, start=0):
        facts.append(f"row_target({r},{k}).")

    with open(out_lp, 'w', encoding='utf-8') as f:
        for line in facts:
            f.write(line + "\n")

    print(f"File saved to {out_lp} with {len(facts)} facts.")

if __name__ == "__main__":
    main()