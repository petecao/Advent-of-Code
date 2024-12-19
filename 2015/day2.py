import aocd
from collections import defaultdict
from collections import deque
import functools
import re
import heapq

lines = aocd.get_data(year=2015, day=2)
lines = lines.split('\n')

debug = True

if debug:
    for line in lines:
        print(line)
        
dims = [[int(i) for i in line.strip().split('x')] for line in lines]
ans = 0
ans2 = 0
for box in dims:
    faces = [box[0] * box[1], box[1] * box[2], box[0] * box[2]]
    perimeters = [2 * (box[0] + box[1]), 2 * (box[1] + box[2]), 2 * (box[0] + box[2])]
    ans += 2 * sum(faces) + min(faces)
    ans2 += min(perimeters) + box[0] * box[1] * box[2]
    
print(ans)
print(ans2)