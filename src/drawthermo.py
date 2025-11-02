import pygame
import sys
import os

def windowdata(lits):
    params={'h':200,'w':400,'caption':''}
    for l in lits:
        for e in thatoms[l]:
            if e[0]=='window':
                for t in e[1:]:
                    if t[0] in params:
                        if type(t[1])==str:
                            params[t[0]]=t[1][1:-1]
                        else:
                            params[t[0]]=t[1]
                return params
    return params

def getvalue(dict,attr,default):
    if attr in dict: return dict[attr]
    return default

### Main program

if len(sys.argv)<2:
    print("drawthermo.py <domainfile.txt> <solution_file.txt>")
    sys.exit()

# Opening files
f = open(sys.argv[1], "r", encoding="utf-8-sig")
domain = [line.strip() for line in f if line.strip() != ""]
f.close()
f = open(sys.argv[2], "r", encoding="utf-8-sig")
filled = [line.strip().replace(" ", "") for line in f if line.strip() != ""]
f.close()

# Extract size and targets
col_targets = [int(x) for x in domain[-2].split()]
row_targets = [int(x) for x in domain[-1].split()]
domain = domain[:-2]
n = len(domain)

# Check
if len(filled) != n or any(len(r) != n for r in filled):
    print("Error: dimensiones de solución y dominio no coinciden.")
    sys.exit(1)

name={'R':'r', 'U':'u', 'L':'l', 'D':'d', '>':'rend', '<':'lend', '^':'uend', 'v':'dend'}

# Visualization
pygame.init()

max_window_size = 900
cellsize = max(40, min(80, max_window_size // (n + 2)))
margin_left = int(cellsize * 1)
margin_top = int(cellsize * 1)
padding = int(cellsize * 0.6)
img_scale = 0.9
screen_w = margin_left + n * cellsize + padding
screen_h = margin_top + n * cellsize + padding
screen = pygame.display.set_mode([screen_w, screen_h])
pygame.display.set_caption("Thermometers puzzle")
screen.fill(pygame.Color("white"))

# Font for row/column numbers
font = pygame.font.SysFont("arial", max(20, cellsize // 2), bold=True)

### Draw thermometers
for i in range(n):
    for j in range(n):
        ch = domain[i][j]
        if ch == '>' and j < n - 1 and domain[i][j+1] == '>': s = 'hor'
        elif ch == '<' and j > 0 and domain[i][j-1] == '<': s = 'hor'
        elif ch == '^' and i > 0 and domain[i-1][j] == '^': s = 'vert'
        elif ch == 'v' and i < n - 1 and domain[i+1][j] == 'v': s = 'vert'
        else: s = name.get(ch, None)
        
        # Load and scale image
        if filled[i][j] == 'x': s = "red-" + s
        img = pygame.image.load("pics/" + s + ".png").convert_alpha()
        scaled = int(cellsize * img_scale)
        img = pygame.transform.smoothscale(img, (scaled, scaled))
        offset = (cellsize - scaled) // 2
        x = margin_left + j * cellsize + offset
        y = margin_top + i * cellsize + offset
        screen.blit(img, [x, y])

### Draw grid lines
line_color = (200, 200, 200)
for i in range(n + 1):
    y = margin_top + i * cellsize
    pygame.draw.line(screen, line_color,
                     (margin_left, y), (margin_left + n * cellsize, y), 2)
for j in range(n + 1):
    x = margin_left + j * cellsize
    pygame.draw.line(screen, line_color,
                     (x, margin_top), (x, margin_top + n * cellsize), 2)
    
### Draw row and column targets
# Columns (top)
for j, val in enumerate(col_targets):
    text = font.render(str(val), True, (0,0,0))
    rect = text.get_rect(center=(margin_left + j * cellsize + cellsize/2, margin_top / 2))
    screen.blit(text, rect)

# Rows (left)
for i, val in enumerate(row_targets):
    text = font.render(str(val), True, (0,0,0))
    rect = text.get_rect(center=(margin_left / 2, margin_top + i * cellsize + cellsize/2))
    screen.blit(text, rect)

### Save and display image
pygame.display.flip()
out_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]
out_path = f"solutions/sol_{out_name}.png"
pygame.image.save(screen, out_path)
print(f"Image saved to {out_path}")

done=False
while not done:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            done = True
pygame.quit()