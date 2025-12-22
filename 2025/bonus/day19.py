from collections import defaultdict, deque
import functools
import re
import heapq
import bisect
import sys

sample_input_1 = '''19532
36182
93847
85364
17385

123
456
789'''
debug = False

with open('day19.input') as f:
    lines = f.read().strip().split('\n\n')
    

    
if debug:
    lines = sample_input_1.strip().split('\n\n')
    print(lines)
    
grids = [block.split('\n') for block in lines]
for i in range(len(grids)):
    grids[i] = [list(map(int, list(line))) for line in grids[i]]
if debug:
    print(grids)
    
memo = defaultdict(int)
def dp(grid_idx, x, y):
    if (grid_idx, x, y) in memo:
        return memo[(grid_idx, x, y)]
    if grid_idx == len(grids):
        return 0
    grid = grids[grid_idx]
    if x >= len(grid) or y >= len(grid[0]):
        return 0
    take_here = grid[x][y]
    go_down = dp(grid_idx, x + 1, y)
    go_right = dp(grid_idx, x, y + 1)
    memo[(grid_idx, x, y)] = take_here + max(go_down, go_right)
    return memo[(grid_idx, x, y)]

ans = 1
for i in range(len(grids)):
    result = dp(i, 0, 0)
    ans *= result

print(ans)

memo_ij_to_top_left = defaultdict(int)
memo_ij_to_bottom_right = defaultdict(int)
memo_ij_to_top_right = defaultdict(int)
memo_ij_to_bottom_left = defaultdict(int)

def dp_ij_to_top_left(grid_idx, i, j):
    if (grid_idx, i, j) in memo_ij_to_top_left:
        return memo_ij_to_top_left[(grid_idx, i, j)]
    if i < 0 or j < 0:
        return 0
    grid = grids[grid_idx]
    take_here = grid[i][j]
    best_prev = max(dp_ij_to_top_left(grid_idx, i-1, j), dp_ij_to_top_left(grid_idx, i, j-1))
    memo_ij_to_top_left[(grid_idx, i, j)] = take_here + best_prev
    return memo_ij_to_top_left[(grid_idx, i, j)]

def dp_ij_to_bottom_right(grid_idx, i, j):
    if (grid_idx, i, j) in memo_ij_to_bottom_right:
        return memo_ij_to_bottom_right[(grid_idx, i, j)]
    grid = grids[grid_idx]
    if i >= len(grid) or j >= len(grid[0]):
        return 0
    take_here = grid[i][j]
    best_prev = max(dp_ij_to_bottom_right(grid_idx, i+1, j), dp_ij_to_bottom_right(grid_idx, i, j+1))
    memo_ij_to_bottom_right[(grid_idx, i, j)] = take_here + best_prev
    return memo_ij_to_bottom_right[(grid_idx, i, j)]

def dp_ij_to_top_right(grid_idx, i, j):
    if (grid_idx, i, j) in memo_ij_to_top_right:
        return memo_ij_to_top_right[(grid_idx, i, j)]
    if i < 0 or j >= len(grids[grid_idx][0]):
        return 0
    grid = grids[grid_idx]
    take_here = grid[i][j]
    best_prev = max(dp_ij_to_top_right(grid_idx, i-1, j), dp_ij_to_top_right(grid_idx, i, j+1))
    memo_ij_to_top_right[(grid_idx, i, j)] = take_here + best_prev
    return memo_ij_to_top_right[(grid_idx, i, j)]

def dp_ij_to_bottom_left(grid_idx, i, j):
    if (grid_idx, i, j) in memo_ij_to_bottom_left:
        return memo_ij_to_bottom_left[(grid_idx, i, j)]
    grid = grids[grid_idx]
    if i >= len(grid) or j < 0:
        return 0
    take_here = grid[i][j]
    best_prev = max(dp_ij_to_bottom_left(grid_idx, i+1, j), dp_ij_to_bottom_left(grid_idx, i, j-1))
    memo_ij_to_bottom_left[(grid_idx, i, j)] = take_here + best_prev
    return memo_ij_to_bottom_left[(grid_idx, i, j)]

ans2 = 1
for grid_idx in range(len(grids)):
    candidate = 0
    grid = grids[grid_idx]
    for i in range(1,len(grid)-1):
        for j in range(1,len(grid[0])-1):
            val = 2 * grid[i][j]
            tl1 = dp_ij_to_top_left(grid_idx, i, j-1)
            br1 = dp_ij_to_bottom_right(grid_idx, i, j+1)
            bl1 = dp_ij_to_bottom_left(grid_idx, i+1, j)
            tr1 = dp_ij_to_top_right(grid_idx, i-1, j)
            candidate1 = val + tl1 + br1 + bl1 + tr1
            tl2 = dp_ij_to_top_left(grid_idx, i-1, j)
            br2 = dp_ij_to_bottom_right(grid_idx, i+1, j)
            bl2 = dp_ij_to_bottom_left(grid_idx, i, j-1)
            tr2 = dp_ij_to_top_right(grid_idx, i, j+1)
            candidate2 = val + tl2 + br2 + bl2 + tr2
            candidate_tmp = max(candidate1, candidate2)
            if candidate_tmp > candidate:
                candidate = candidate_tmp
    ans2 *= candidate
print(ans2)