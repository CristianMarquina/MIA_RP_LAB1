import sys
import json
import os

# CONFIGURACIÓN DE ARCHIVOS
file_name = input("Ingresa el nombre del archivo de entrada (por ejemplo dom07.txt): ")  # Nombre del archivo de entrada
in_path = os.path.join(".", "examplesthermo", file_name)

output_file = input("Ingresa el nombre del archivo de salida (por ejemplo dom07.json): ")  # Nombre del archivo de salida
output_dir = os.path.join(".", "instances")
os.makedirs(output_dir, exist_ok=True)

out_path = os.path.join(output_dir, output_file)

# SIMBOLOS
# Tramos rectos (misma semántica que la versión recta)
ARROWS = {'^': (-1, 0), 'v': (1, 0), '>': (0, 1), '<': (0, -1)}

# Bulbos (dirección inicial)
BULBS  = {'U': (-1, 0), 'D': (1, 0), 'R': (0, 1), 'L': (0, -1)}

# Giros (curvas) como en el enunciado: 0,1,2,3 = └ ┏ ┐ ┘  (rotaciones)
# Mapa: (dir_entrada) -> (dir_salida)
# Convención: Up=(-1,0), Down=(1,0), Right=(0,1), Left=(0,-1)
CORNER_TURNS = {
    '0': { (1,0):(0,1),  (0,-1):(-1,0) },   # └ : de Down→Right, de Left→Up
    '1': { (-1,0):(0,1), (0,-1):(1,0) },    # ┏ : de Up→Right,  de Left→Down
    '2': { (-1,0):(0,-1),(0,1):(1,0) },     # ┐ : de Up→Left,   de Right→Down
    '3': { (1,0):(0,-1), (0,1):(-1,0) }     # ┘ : de Down→Left, de Right→Up
}

def in_bounds(n, r, c): # Comprueba si una posición (r, c) está dentro de los límites de la cuadrícula n×n.
    return 0 <= r < n and 0 <= c < n

def read_instance(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    if len(lines) < 3:
        print("Error: la entrada es demasiado corta.")
        sys.exit(1)

    col_line = lines[-2].strip()
    row_line = lines[-1].strip()
    
    try:
        col_sums = [int(x) for x in col_line.split()]
        row_sums = [int(x) for x in row_line.split()]
    except ValueError:
        print("Error: las dos últimas líneas deben contener enteros separados por espacios.")
        sys.exit(1)

    n = len(col_sums)
    assert n == len(row_sums), "Sumas de filas/columnas con distinto tamaño"

    grid_lines = lines[:-2]
    assert len(grid_lines) == n, f"Se esperaban {n} filas de rejilla y hay {len(grid_lines)}"
    
    grid = [list(row) for row in grid_lines]
    for r in range(n):
        assert len(grid[r]) == n, f"Fila {r} no tiene {n} columnas"
    return grid, col_sums, row_sums

def from_bulb_curved(grid, r, c, dr, dc):
    """
    Sigue el termómetro desde (r,c) con dirección (dr,dc):
    - Si encuentra un tramo recto, continúa recto (símbolo coherente con la dirección).
    - Si encuentra un giro 0/1/2/3, cambia la dirección según CORNER_TURNS.
    - Se detiene cuando ya no puede avanzar (fuera o símbolo incompatible).
    Devuelve lista de celdas [(r0,c0),(r1,c1),...], empezando por el bulbo.
    """
    n = len(grid)
    path = [(r, c)]
    
    direct = {(-1,0):'^', (1,0):'v', (0,1):'>', (0,-1):'<'}
    rr, cc = r + dr, c + dc
    cur_dr, cur_dc = dr, dc

    while in_bounds(n, rr, cc):
        ch = grid[rr][cc]

        if ch in ARROWS:
         # debe coincidir con la dirección actual
            if ch != direct[(cur_dr, cur_dc)]:
                break
            path.append((rr, cc))
            rr += cur_dr
            cc += cur_dc
            continue

        elif ch in CORNER_TURNS:
            turn_map = CORNER_TURNS[ch]

            # la dirección de *entrada* a la celda es la dirección de movimiento actual
            entry_dir = (cur_dr, cur_dc)

            if entry_dir not in turn_map:
            # Curva incompatible: el termómetro termina antes de esta celda
                break

            path.append((rr, cc))
        # nueva dirección tras el giro
            cur_dr, cur_dc = turn_map[entry_dir]  # nueva dirección tras el giro
            rr += cur_dr
            cc += cur_dc
            continue

        else:
        # cualquier otra cosa detiene el termómetro
            break

    return path

def build_thermos(grid):
    """
    Encuentra bulbos y construye paths (con posibles giros).
    Valida:
      1) No solapamientos.
      2) Toda celda simbólica (bulbo/recto/giro) pertenece a algún path.
    """
    n = len(grid)
    bulbs = []
    thermo_paths = []
    used = set()

    # localizar bulbos
    for r in range(n):
        for c in range(n):
            ch = grid[r][c]
            if ch in BULBS:
                bulbs.append((r, c, *BULBS[ch]))

    # seguir cada bulbo
    for (r, c, dr, dc) in bulbs:
        path = from_bulb_curved(grid, r, c, dr, dc)

        for (pr, pc) in path:
            if (pr, pc) in used:
                raise AssertionError(f"Solapamiento: celda {pr},{pc} pertenece a >1 termómetro")
            used.add((pr, pc))
        thermo_paths.append(path)

    # Validación: cualquier símbolo de la rejilla relacionado con termómetros
    # debe estar en algún path (bulbos, rectos, giros)
    for r in range(n):
        for c in range(n):
            ch = grid[r][c]
            if ch in BULBS or ch in ARROWS or ch in CORNER_TURNS:
                if (r, c) not in used:
                    print(f"Error: celda {r},{c} con símbolo '{ch}' no conectada a ningún bulbo.")
                    sys.exit(1)
                    
    return bulbs, thermo_paths

def main():
    # Leer archivo
    grid, col_sums, row_sums = read_instance(in_path)

    # Construir termómetros
    bulbs, thermo_paths = build_thermos(grid)

    # Formato JSON
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
    # Guardar archivo JSON
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

    print("Conversión completada correctamente.")
    print(f"Archivo JSON guardado en: {out_path}")
    print(f"Tamaño de la cuadrícula: {n}x{n}")
    print(f"Se detectaron {len(thermos_json)} termómetros.")

if __name__ == "__main__":
    main()
