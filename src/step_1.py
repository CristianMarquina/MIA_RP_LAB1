# Objetivo del step 1:
#     Leer los archivos ASCII (dom01.txt por ejemplo)
#     Definir significado de caracteres
#     Especificar la estructura del archivo de entrada

import os
import json
import sys

file_name = input("Ingresa el nombre del archivo de entrada (por ejemplo dom01): ")
output_file = file_name  # input("Ingresa el nombre del archivo de salida (por ejemplo dom01.json): ")
file_name = file_name + ".txt"
output_file = output_file + ".json"

in_path = os.path.join(".", "examplesthermo", file_name)
output_dir = os.path.join(".", "examplesthermo")

out_path = os.path.join(output_dir, output_file)

symbols = {"^" : (-1,0), "v" : (1,0), "<" : (0,-1), ">" : (0,1)}
bulbs = {"U" : (-1,0), "D" : (1,0), "L" : (0,-1), "R" : (0,1)}

def in_bounds(n, r, c):   # Comprobar si filas y columnas están dentro de n
    if r < 0 or r >= n: # Verificamos si la fila (r) está dentro de n(tamañp)
        return False
    
    if c < 0 or c >= n: # Verificamos si la columna (c) está dentro de n(tamañp)
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

    # Tenemos que convertir estos valores en numeros enteros
    col_sum = []
    for i in col_line.split():
        col_sum.append(int(i))

    row_sum = []
    for i in row_line.split():
        row_sum.append(int(i))

    # El tamaño es de tipo (n x n)
    n = len(col_sum)
    assert n == len(row_sum), "Sumas de filas/columnas con distinto tamaño"
    
    # Obtenemos la cuadricula que nos interesa
    grid_lines = lines[:-2]
    assert len(grid_lines) == n, f"Se esperaban {n} filas de rejilla y hay {len(grid_lines)}"
    
    grid = []
    for row in grid_lines:
        grid.append(list(row))

    # Comprobar que cada fila tien el numero correcto de columnas
    for i in range(n):
        if len(grid[i]) != n:
            print(f"Error: the row {i} does not have {n} columns")
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
        print("Error: dirección de bulbo inválida.")
        return None
    
    # Calculamos la nueva posición
    rr = r + rd
    cc = c + cd
    while in_bounds(n, rr, cc) and grid[rr][cc] == seg: #mientras que estemos dentro de los límites y el símbolo sea correcto
        path.append((rr, cc))
        # Actualizamos la posición // avanzamos en la dirección del bulbo
        rr += rd
        cc += cd

    return path


def thermos(grid):    #Encuentra bulbos, construye paths completos y valida que no se crucen ni cambien de dirección.
    n = len(grid)

    # Listas para guardar resultados
    found_bulbs = []
    thermo_paths = []   
    used = set()        # Conjunto de celdas ya usadas (para detectar solapamientos)
    
    # encontrar bulbos
    for r in range(n):
        for c in range(n):
            ch = grid[r][c]
            if ch in bulbs: # Ahora 'bulbs' es el diccionario global
                rd, cd = bulbs[ch]
                if (r, c) in used:
                    continue

                path = from_bulbs(grid, r, c, rd, cd) # Obtener el path desde el bulbo
                # Comprobar solapamientos
                for (row, col) in path:
                    if (row, col) in used:
                        print("Error: thermos paths overlap at cell", (row, col))
                        return None
                    used.add((row, col)) # Añadir la celda al conjunto de usadas
                found_bulbs.append((r, c, rd, cd))
                thermo_paths.append(path)

        # Verificar que no haya celdas en blank
    for r in range(n):
        for c in range(n):
            ch = grid[r][c]
            if ch in bulbs or ch in symbols:
                if (r, c) not in used:
                    print(f"Error: cell {r},{c} with symbol '{ch}' not connected to any bulb")
                    return None
                    
    return found_bulbs, thermo_paths  

def main():
    # if len(sys.argv) != 3:
    #     print("Uso: python3 step1_parse.py domXX.txt instance.json")
    #     sys.exit(1)
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