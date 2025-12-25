from collections import defaultdict, deque
import functools
from math import ceil, floor
import re
import heapq
import networkx as nx
from ortools.sat.python import cp_model

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
...#
....
....
#...

5x12: 1 0 1 0 2 2
####......#.
#...........
............
....####...#
...##..#.#.#

5x12: 1 0 1 0 3 2
............
............
............
............
............
'''

debug = False

with open('day25.input') as f:
    lines = f.read().strip().split('\n\n')
    
if debug:
    lines = sample_input_1.strip().split('\n\n')
    print(lines)
    
patterns = lines[:6]
# count number of '#' in each pattern
count_of_hashes = []
for p in patterns:
    count = sum(1 for line in p.split('\n')[1:] for ch in line if ch == '#')
    count_of_hashes.append(count)
if debug:
    print("Patterns:")
    print(patterns)
    print("Count of # in each pattern:", count_of_hashes)
    
    
grids_info = lines[6:]
split_grids = []
for g in grids_info:
    split_grids.append(g.split('\n'))
    
grid_metadata = [g[0] for g in split_grids]
grids = [g[1:] for g in split_grids]

grid_metadata_temp = []
for meta in grid_metadata:
    size_part, pattern_counts_part = meta.split(':')
    rows, cols = map(int, size_part.split('x'))
    pattern_counts = list(map(int, pattern_counts_part.strip().split()))
    pattern_counts = sum(pattern_counts)
    grid_metadata_temp.append((rows, cols, pattern_counts))
grid_metadata = grid_metadata_temp
if debug:
    print(grid_metadata)

count_of_hashes_per_grid = []
for grid in grids:
    count = sum(1 for line in grid for ch in line if ch == '#')
    count_of_hashes_per_grid.append(count)
if debug:
    print("Count of # in each grid:", count_of_hashes_per_grid)
    
area_per_grid = []
for (rows, cols, pattern_counts) in grid_metadata:
    area_per_grid.append(rows * cols)
    
ans = 0
for i in range(len(grids)):
    grid = grids[i]
    dominoes = grid_metadata[i][2]
    rows = len(grid)
    cols = len(grid[0])
    # can we fit vert vertical dominoes and horiz horizontal dominos in the empty spaces?
    
    # free_cells = sum(1 for r in range(rows) for c in range(cols) if grid[r][c] != '#')
    # if free_cells < 2 * (vert + horiz):
    #     continue
    
    def can_fit_dominoes(grid, target):
        rows = len(grid)
        cols = len(grid[0])
        G = nx.Graph()
        top_nodes = set()
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '#':
                    continue
                is_white = (r + c) % 2 == 0
                node = (r, c)
                G.add_node(node)
                if is_white:
                    top_nodes.add(node)
                    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
                            G.add_edge((r, c), (nr, nc))
                            
                
        matching = nx.bipartite.maximum_matching(G, top_nodes=top_nodes)
        
        max_dominoes = len(matching) // 2
        return max_dominoes >= target
    
    if can_fit_dominoes(grid, dominoes):
        ans += (i+1)
    
print(ans)