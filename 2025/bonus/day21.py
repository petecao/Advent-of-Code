from collections import defaultdict, deque
import functools
import itertools
from math import ceil, floor
import re
import heapq

sample_input_1 = '''#####
#O#.#
#...O
#.#.#
#####

###O#
#O#.#
#.#.#
#...#
##.##

#####
#####
#####
#####
#####

#####
#####
#####
#####
#####

#####
#####
#####
#####
#####

#####
#####
#####
#####
#####
'''

debug = False

with open('day21.input') as f:
    grids = f.read().strip().split('\n\n')
    
if debug:
    grids = sample_input_1.strip().split('\n\n')
    print(grids)
    
grids_parsed = []
for grid in grids:
    grid_lines = grid.split('\n')
    grid_parsed = []
    for line in grid_lines:
        grid_parsed.append(list(line))
    grids_parsed.append(grid_parsed)
    
if debug:
    for grid in grids_parsed:
        for line in grid:
            print(''.join(line))
        print()
                
# find locations of O in each grid
grids_O_positions = []
for grid in grids_parsed:
    O_positions = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 'O':
                O_positions.append((r, c))
    grids_O_positions.append(O_positions)
    
if debug:
    for O_positions in grids_O_positions:
        print(O_positions)
        
# find distances between the two O's avoiding "#"
def bfs_distance(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])
    queue = deque([(start, 0)])
    visited = set()
    visited.add(start)
    while queue:
        (current, dist) = queue.popleft()
        if current == goal:
            return dist
        (r, c) = current
        for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), dist + 1))
    return float('inf')  # unreachable

grid_distances = []
for O_positions, grid in zip(grids_O_positions, grids_parsed):
    if len(O_positions) < 2:
        grid_distances.append(float('inf'))
    else:
        dist = bfs_distance(grid, O_positions[0], O_positions[1])
        grid_distances.append(dist)
        
# if debug:
    # print(grid_distances)
    
ans = 1
for dist in grid_distances:
    ans *= (dist-1)
print(ans)

assert len(grids) == 6
# find the configuration that yields a valid cube net from the 6 square grids

# get the edge of each grid
grid_edges = []
for grid in grids_parsed:
    top = ''.join(grid[0])
    bottom = ''.join(grid[-1])
    left = ''.join([grid[r][0] for r in range(len(grid))])
    right = ''.join([grid[r][-1] for r in range(len(grid))])
    grid_edges.append((top, right, bottom, left))

# if debug:
    # print("Grid edges:")
    # for edges in grid_edges:
    #     print(edges)
    # print()

edge_matches = defaultdict(list)
for i in range(len(grid_edges)):
    for j in range(len(grid_edges)):
        if i != j:
            for i_idx in range(4):
                edge_i = grid_edges[i][i_idx]
                if set(edge_i) == {'#'}:
                    continue
                for j_idx in range(4):
                    edge_j = grid_edges[j][j_idx]
                    if set(edge_j) == {'#'}:
                        continue
                    if edge_i == edge_j or edge_i == edge_j[::-1]:
                        edge_matches[(i, i_idx)].append((j, j_idx))
                        
# if debug:
    # for k, v in edge_matches.items():
    #     print(f'Grid {k} matches with grids {v}')
    
# cube net adjacency
cube_net_adjacency = {0: [1, 2, 3, 4],
                      1: [0, 2, 5, 4],
                      2: [0, 1, 5, 3],
                      3: [0, 2, 5, 4],
                      4: [0, 1, 5, 3],
                      5: [1, 2, 3, 4]}
    
def rotate_grid(grid):
    return [''.join([grid[len(grid) - 1 - c][r] for c in range(len(grid))]) for r in range(len(grid[0]))]

grids_parsed = []
for grid in grids:
    grid_lines = grid.split('\n')
    grid_parsed = []
    for line in grid_lines:
        grid_parsed.append(list(line))
    grids_parsed.append(grid_parsed)
with open('day21_output.txt', 'w') as f:
    for grid_idx, grid in enumerate(grids_parsed):
        current_grid = [''.join(row) for row in grid]
        for rotation in range(4):
            f.write(f'Grid {grid_idx} rotation {rotation}:\n')
            for line in current_grid:
                f.write(line + '\n')
            f.write('\n')
            current_grid = rotate_grid(current_grid)
            
# indexes: front, top, right, left, bottom, back

final_configuration = {0: (4, 0), # front
                        1: (5, 0), # top
                        2: (0, 0), # right
                        3: (3, 1), # left
                        4: (2, 1), # bottom
                        5: (1, 1)} # back

        
with open('day21_final_net.txt', 'w') as f:
    size = len(grids_parsed[0])
    net_rows = 3 * size
    net_cols = 4 * size
    net_grid = [[' ' for _ in range(net_cols)] for _ in range(net_rows)]
    
    position_to_coords = {
        0: (size, size),      # front
        1: (0, 2*size),         # top
        2: (size, 2 * size),  # right
        3: (size, 0),         # left
        4: (2 * size, size),  # bottom
        5: (0, 3*size)   # back
    }
    
    for pos_idx, (sq_idx, rot) in final_configuration.items():
        grid = grids_parsed[sq_idx]
        for _ in range(rot):
            grid = rotate_grid([''.join(row) for row in grid])
            grid = [list(row) for row in grid]
        
        start_r, start_c = position_to_coords[pos_idx]
        for r in range(size):
            for c in range(size):
                net_grid[start_r + r][start_c + c] = grid[r][c]
    
    for row in net_grid:
        f.write(''.join(row) + '\n')
        
with open('day21_final_net.txt', 'r') as f:
    large_grid = f.read().split('\n')[:-1]
    
large_grid = [list(line) for line in large_grid]
row_lens = [len(row) for row in large_grid]
assert all(l == row_lens[0] for l in row_lens)

# find positions of O in large grid
O_positions_large = []
for r in range(len(large_grid)):
    for c in range(len(large_grid[0])):
        if large_grid[r][c] == 'O':
            O_positions_large.append((r, c))
            
assert len(O_positions_large) == 12
# if debug:

start = O_positions_large[0]
paths = {}
queue = deque([(start, {start})])
while queue:
    (current, path) = queue.popleft()
    if current in paths:
        continue
    paths[current] = path
    r, c = current
    for (dr, dc) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr = r + dr
        nc = c + dc
        if 0 <= nr < len(large_grid) and 0 <= nc < len(large_grid[0]) and large_grid[nr][nc] != '#':
            npos = (nr, nc)
            if npos not in path:
                new_path = path | {npos}
                queue.append((npos, new_path))
    
ans = len({p for end in O_positions_large for p in paths[end]}) - 12
print(ans)