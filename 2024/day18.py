from math import floor
import aocd
from collections import defaultdict
from collections import deque
import functools
import re
import heapq

sample_input_1 = ''''''

lines = aocd.get_data(year=2024, day=18)
lines = lines.split('\n')

debug = True
        
row_cols = [(int(i.split(',')[1]), int(i.split(',')[0])) for i in lines]
curr_obstacles = set(row_cols[:1024])

num_rows = 71
num_cols = 71

def is_in_bounds(row, col):
    return 0 <= row < num_rows and 0 <= col < num_cols

steps = [(0, 1), (0, -1), (1, 0), (-1, 0)]

pq = []
heapq.heappush(pq, (0, 0, 0))
node_costs = defaultdict(lambda: float('inf'))

while pq:
    cost, row, col = heapq.heappop(pq)
    if (row, col) == (num_rows - 1, num_cols - 1):
        print(cost)
        break
    if node_costs[(row, col)] <= cost:
        continue
    node_costs[(row, col)] = cost
    for step in steps:
        new_row = row + step[0]
        new_col = col + step[1]
        if is_in_bounds(new_row, new_col) and (new_row, new_col) not in curr_obstacles:
            heapq.heappush(pq, (cost + 1, new_row, new_col))
            
for i in range(1025, len(row_cols)):
    curr_obstacles.add(row_cols[i])
    pq = []
    heapq.heappush(pq, (0, 0, 0))
    node_costs = defaultdict(lambda: float('inf'))
    path_found = False
    while pq:
        cost, row, col = heapq.heappop(pq)
        if (row, col) == (num_rows - 1, num_cols - 1):
            path_found = True
            break
        if node_costs[(row, col)] <= cost:
            continue
        node_costs[(row, col)] = cost
        for step in steps:
            new_row = row + step[0]
            new_col = col + step[1]
            if is_in_bounds(new_row, new_col) and (new_row, new_col) not in curr_obstacles:
                heapq.heappush(pq, (cost + 1, new_row, new_col))
                
    if not path_found:
        print(row_cols[i][1], row_cols[i][0])
        break