import aocd
from collections import defaultdict
from collections import deque
import functools
import re
import heapq

lines = aocd.get_data(year=2015, day=6)
lines = lines.split('\n')

debug = True

if debug:
    for line in lines:
        print(line)
        
grid = [[0 for i in range(1000)] for j in range(1000)]

instructions = [i.split() for i in lines]
new_instructions = []

for i in instructions:
    if i[0] == 'turn':
        new_instructions.append((i[1], i[-3], i[-1]))
    else:
        new_instructions.append((i[0], i[-3], i[-1]))
        
instructions = [(i[0], tuple(map(int, i[1].split(','))), tuple(map(int, i[2].split(',')))) for i in new_instructions]


for instruction in instructions:
    r1, c1 = instruction[1]
    r2, c2 = instruction[2]
    for i in range(r1, r2+1):
        for j in range(c1, c2+1):
            if instruction[0] == 'on':
                grid[i][j] += 1
            elif instruction[0] == 'off':
                grid[i][j] = max(0, grid[i][j] - 1)
            else:
                grid[i][j] += 2
                
ans = sum([sum(i) for i in grid])
print(ans)