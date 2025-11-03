import os
import sys
import subprocess
import clingo

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLES_DIR = os.path.join(BASE_DIR, "..", "examplesthermo")
FACTS_DIR = os.path.join(BASE_DIR, "..", "facts")
SOLUTIONS_DIR = os.path.join(BASE_DIR, "..", "solutions")

STEP1 = os.path.join(BASE_DIR, "step_1.py")
ENCODE = os.path.join(BASE_DIR, "encode.py")
THERMO = os.path.join(BASE_DIR, "thermo.lp")
DRAW = os.path.join(BASE_DIR, "drawthermo.py")

# --- ENSURE FOLDERS EXIST ---
for folder in [FACTS_DIR, SOLUTIONS_DIR]:
    os.makedirs(folder, exist_ok=True)

# --- MAIN ---
if len(sys.argv) < 2:
    print("Usage: python src/main.py examplesthermo/domXX.txt")
    sys.exit(1)

input_txt = sys.argv[1]
if not os.path.exists(input_txt):
    print(f"Input file not found: {input_txt}")
    sys.exit(1)

# File base names
base_name = os.path.splitext(os.path.basename(input_txt))[0]
json_path = os.path.join(EXAMPLES_DIR, f"{base_name}.json")
facts_path = os.path.join(FACTS_DIR, f"{base_name}.lp")
output_txt = os.path.join(SOLUTIONS_DIR, f"solution_{base_name}.txt")

print("Starting full Thermometers pipeline...")
print("-----------------------------------------")


print("Step 1:\nGenerating JSON instance...")
input_name = os.path.splitext(os.path.basename(input_txt))[0]
subprocess.run(["python", STEP1], input=f"{input_name}\n{base_name}.json\n".encode(), check=True)
if not os.path.exists(json_path):
    print("JSON file not generated. Aborting.")
    sys.exit(1)
print(f"JSON created: {json_path}")

print("\nStep 2: \nEncoding to ASP facts...")
subprocess.run(["python", ENCODE, json_path, facts_path], check=True)
if not os.path.exists(facts_path):
    print("Facts file not generated. Aborting.")
    sys.exit(1)
print(f"Facts created: {facts_path}")


print("\nStep 3: \Solving with Clingo (Python module)...")

ctl = clingo.Control()
ctl.load(THERMO)
ctl.load(facts_path)
ctl.ground([("base", [])])

size = 0
fills = []
nummodels = 0

with ctl.solve(yield_=True) as handle:
    for model in handle:
        if nummodels > 0:
            print("MORE THAN ONE MODEL FOUND!")
            break
        for atom in model.symbols(atoms=True):
            if atom.name == "dim" and len(atom.arguments) == 1:
                size = atom.arguments[0].number
            elif atom.name == "fill" and len(atom.arguments) == 2:
                fills.append((atom.arguments[0].number, atom.arguments[1].number))
        nummodels += 1

if nummodels == 0:
    print("UNSATISFIABLE.")
    sys.exit(1)

# Write the solution to a text file
grid = [["."] * size for _ in range(size)]
for (r, c) in fills:
    grid[r][c] = "x"

with open(output_txt, "w", encoding="utf-8") as f:
    for row in grid:
        f.write("".join(row) + "\n")

print(f"Solution saved: {output_txt}")


print("\nStep 4:\nDrawing final puzzle...")
subprocess.run([sys.executable, DRAW, input_txt, output_txt], check=True)
print(f"Drawing completed! Saved to solutions/solution_{base_name}.png")

print("\n-----------------------------------------")
print(f"Completed. Summary:")
print(f"JSON:       {json_path}")
print(f"Facts:      {facts_path}")
print(f"Solution:   {output_txt}")
print(f"Image:      solutions/solutions_{base_name}.png\n")