import aocd
from collections import defaultdict

sample_input = '''89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732'''

lines = aocd.get_data(year=2024, day=10)
lines = lines.split('\n')

lines = [[int(x) for x in line] for line in lines]
    
def is_in_bounds(r, c):
    return r >= 0 and r < len(lines) and c >= 0 and c < len(lines[0])
    

zeroes = []

for r in range(len(lines)):
    for c in range(len(lines[r])):
        if lines[r][c] == 0:
            zeroes.append((r, c))

queue = [] # will contain ((starting_r, starting_c), (current_r, current_c), height)
paths_per_zero = defaultdict(int)

for zero in zeroes:
    queue.append((zero, zero, 0))
    

steps = [(0, 1), (0, -1), (1, 0), (-1, 0)]

while queue:
    start, current, height = queue.pop()
    if not is_in_bounds(current[0], current[1]):
        continue
    if lines[current[0]][current[1]] != height:
        continue
    if lines[current[0]][current[1]] == 9:
        paths_per_zero[start] += 1
        continue
    
    for step in steps:
        new_r = current[0] + step[0]
        new_c = current[1] + step[1]
        queue.append((start, (new_r, new_c), height + 1))
        
sum = 0
for zero in paths_per_zero:
    sum += (paths_per_zero[zero])
    
print(sum)
    