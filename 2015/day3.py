import aocd
from collections import defaultdict
from collections import deque
import functools
import re
import heapq

lines = aocd.get_data(year=2015, day=3)
lines = lines.split('\n')

debug = True

if debug:
    for line in lines:
        print(line)
    print(len(lines))
        
visited = set([(0,0)])
visited2 = set([(0,0)])

x, y = 0, 0
x2, y2 = 0, 0
# line = '^v^v^v^v^v'
line = lines[0]

dir_map = {'^': (0, 1), 'v': (0, -1), '<': (-1, 0), '>': (1, 0)}
for i in range(0,len(line),2):
    symbol = line[i]
    symbol2 = line[i+1]
    dx, dy = dir_map[symbol]
    x += dx
    y += dy
    visited.add((x, y))
    dx2, dy2 = dir_map[symbol2]
    x2 += dx2
    y2 += dy2
    visited2.add((x2, y2))
    
print(len(visited | visited2))