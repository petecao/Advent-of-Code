from collections import defaultdict
import aocd
import functools
import re

sample_input_1 = '''0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2'''

lines = aocd.get_data(year=2025, day=12)

debug = False

if not debug:
    shapes =  lines.split('\n\n')
else:
    shapes  = sample_input_1.split('\n\n')
    
# lines = lines.split('\n')

if debug:
    print(shapes)
    
grids = shapes[-1]

num_filled = [sum([row.count('#') for row in grid]) for grid in shapes[:-1]]
print(grids)
print(num_filled)

dims = [list(map(int, dim.split('x'))) for dim in re.findall(r'(\d+x\d+):', grids)]
print(dims)
items = [list(map(int, re.findall(r': (.+)', grid)[0].split(' '))) for grid in re.findall(r'(\d+x\d+: .+)', grids)]
print(items)

ans = 0
for i in range(len(dims)):
    w, h = dims[i]
    count = items[i]
    area = w * h
    total_filled = 0
    for j in range(len(count)):
        total_filled += count[j] * num_filled[j]
    if area > total_filled:
        ans += 1
print(ans)