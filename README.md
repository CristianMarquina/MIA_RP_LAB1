# MIA_RP_LAB1

This project provides a complete pipeline to solve the Thermometers puzzle using ASP (Answer Set Programming) and Python. The main script is `src/main.py`.

## What does the code do?

The pipeline consists of four main steps:

1. **Convert ASCII instance to JSON**  
	Reads an input file (e.g., `examplesthermo/dom01.txt`) and generates a structured JSON file describing the puzzle grid, thermometers, bulbs, and target sums.

2. **Encode JSON to ASP facts**  
	Converts the JSON file into ASP facts (`.lp` format) for use with the Clingo solver.

3. **Solve the puzzle using Clingo**  
	Loads the ASP encoding and facts, solves the puzzle, and writes the solution (filled grid) to a text file.

4. **Draw the solution**  
	Uses a drawing script to generate a visual representation of the solution as an image.

## How to run the code?

1. **Requirements**:
	- Python 3
	- Create the environment and install the requirements. `pip install -r requirements.txt`)
	- All scripts in `src/` and required input files in `examplesthermo/` and `examplesthermo_curved/`

2. **File locations**:
	- Input files: `examplesthermo/domXX.txt`
	- Main script: `src/main.py`

3. **Run the pipeline**:
	- Open a terminal in the project root directory.
	- Run the main script with:
	  ```
	  python src/main.py examplesthermo/dom01.txt
	  ```
	- The script will automatically:
	  - Generate `examplesthermo/dom01.json`
	  - Generate `facts/dom01.lp`
	  - Generate `solutions/solution_dom01.txt`
	  - Generate `solutions/solution_dom01.png`

4. **Output**:
	- The solution files and image will be saved in the `solutions/` folder.

## Example usage

Suppose you have the file `examplesthermo/dom01.txt`. Run:

```
python src/main.py examplesthermo/dom01.txt
```

The results will be:
- JSON: `examplesthermo/dom01.json`
- ASP facts: `facts/dom01.lp`
- Solution grid: `solutions/solution_dom01.txt`
- Solution image: `solutions/solution_dom01.png`

## How to run each step individually

You can execute each part of the pipeline manually, which is useful for debugging or for more control over the process.

### Standard Flow

1. **Step 1: Convert ASCII to JSON**
   ```bash
   python src/step_1.py
   ```
   - When prompted, enter the base name of your input file (e.g., `dom01`).
   - Output: `examplesthermo/dom01.json`

2. **Step 2: Encode JSON to ASP facts**
   ```bash
   python src/encode.py examplesthermo/dom01.json facts/dom01.lp
   ```
   - Output: `facts/dom01.lp`

3. **Step 3: Solve with Clingo (Potassco)**
   ```bash
   conda activate potassco
   clingo 0 src/thermo.lp facts/dom01.lp > solutions/solution_dom01.txt
   ```
   - Output: `solutions/solution_dom01.txt`

4. **Step 4: Draw the solution**
   ```bash
   python src/drawthermo.py examplesthermo/dom01.txt solutions/solution_dom01.txt
   ```
   - Output: `solutions/solution_dom01.png`

---

### Optional Flow

If you want to use the optional step (e.g., for alternative parsing or preprocessing):

1. **Step 1 (Optional): Convert ASCII to JSON with alternative script**
   ```bash
   python src/step_1_optional.py
   ```
   - When prompted, enter the base name of your input file (e.g., `dom01`).
   - Output: `examplesthermo_curved/dom01.json`

2. **Step 2: Encode JSON to ASP facts**
   ```bash
   python src/encode.py examplesthermo_curved/dom01.json facts/dom01.lp
   ```

3. **Step 3: Solve with Clingo**
   ```bash
   clingo 0 src/thermo.lp facts/dom01.lp > solutions/solution_dom01.txt
   ```

---

**Note:**  
- Replace `dom01` with your actual instance name.  
- Make sure all scripts are run from the project root directory.  
- The Clingo command (`clingo`) requires Potassco’s Clingo to be installed and available in your PATH.

---
