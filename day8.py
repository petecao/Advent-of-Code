import aocd
from collections import defaultdict
from math import gcd


lines = aocd.get_data(year=2024, day=8)
lines = lines.split('\n')
    
def is_out_of_bounds(x,y):
    return x < 0 or y < 0 or x >= len(lines) or y >= len(lines[0])
    
all_symbols = defaultdict(list)

for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] != '.':
            all_symbols[lines[i][j]].append((i,j))
            
points = set()
            
for symbol in all_symbols:
    print(all_symbols[symbol])
    for i in range(len(all_symbols[symbol])):
        for j in range(i+1, len(all_symbols[symbol])):
            x1, y1 = all_symbols[symbol][i]
            x2, y2 = all_symbols[symbol][j]
            
            dx = x2 - x1
            dy = y2 - y1
            
            gcd_val = gcd(dx, dy)
            dx //= gcd_val
            dy //= gcd_val
            
            saved_x1 = x1
            saved_y1 = y1
            
            while not is_out_of_bounds(x1, y1):
                points.add((x1, y1))
                x1 += dx
                y1 += dy
                
            x1 = saved_x1
            y1 = saved_y1
            while not is_out_of_bounds(x1, y1):
                points.add((x1, y1))
                x1 -= dx
                y1 -= dy
            
print(len([point for point in points if not is_out_of_bounds(point[0], point[1])]))