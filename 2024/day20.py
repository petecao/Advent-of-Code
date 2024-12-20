import aocd
from collections import defaultdict
import heapq

sample_input_1 = '''###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############'''

lines = aocd.get_data(year=2024, day=20)
lines = lines.split('\n')

debug = True

if debug:
    for line in lines:
        print(line)
        
def is_in_bounds(row, col):
    return 0 <= row < len(lines) and 0 <= col < len(lines[0])
        
sr, sc = -1, -1
er, ec = -1, -1
for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] == 'S':
            sr, sc = r, c
        if lines[r][c] == 'E':
            er, ec = r, c
            
steps = [(0, 1), (0, -1), (1, 0), (-1, 0)]
pq = []
heapq.heappush(pq, (0, sr, sc))
node_costs = defaultdict(lambda: float('inf'))
shortest_length = 99999999999999999999999999999999999


while pq:
    cost, row, col = heapq.heappop(pq)
    if (row, col) == (er, ec):
        if cost < shortest_length:
            shortest_length = cost
        print(cost)
    if node_costs[(row, col)] < cost:
        continue
    node_costs[(row, col)] = cost
    for step in steps:
        new_row = row + step[0]
        new_col = col + step[1]
        if is_in_bounds(new_row, new_col) and lines[new_row][new_col] != '#':
            heapq.heappush(pq, (cost + 1, new_row, new_col))

# invert node_costs
cost_nodes = {v: k for k, v in node_costs.items()}
assert all(k in cost_nodes for k in range(shortest_length + 1))

num_shortcuts = 0
for i in range(shortest_length):
    row, col = cost_nodes[i]
    for step in steps:
        new_row = row + step[0]
        new_col = col + step[1]
        if is_in_bounds(new_row, new_col) and lines[new_row][new_col] == '#':
            new_row += step[0]
            new_col += step[1]
            if is_in_bounds(new_row, new_col) and lines[new_row][new_col] != '#':
                if node_costs[(new_row, new_col)] - (i + 2) >= 100:
                    num_shortcuts += 1
                    
print(num_shortcuts)

def get_cost_through_wall(r, c):
    temp_node_costs = defaultdict(lambda: float('inf'))
    final_node_costs = defaultdict(lambda: float('inf'))
    pq2 = []
    heapq.heappush(pq2, (0, r, c))
    for step in steps:
        new_row = r + step[0]
        new_col = c + step[1]
    while pq2:
        # print(pq2)
        cost, row, col = heapq.heappop(pq2)
        # print(cost, row, col)
        if cost > 20:
            break
        if temp_node_costs[(row, col)] <= cost:
            continue
        if lines[row][col] != '#' and cost > 1:
            if final_node_costs[(row, col)] > cost:
                final_node_costs[(row, col)] = cost
        temp_node_costs[(row, col)] = cost
        for step in steps:
            new_row = row + step[0]
            new_col = col + step[1]
            if is_in_bounds(new_row, new_col):
                heapq.heappush(pq2, (cost + 1, new_row, new_col))
                
    return final_node_costs
                
num_shortcuts = 0
shortcuts_by_time = defaultdict(int)
for i in range(shortest_length):
    row, col = cost_nodes[i]
    all_shortcuts = get_cost_through_wall(row, col)
    for shortcut in all_shortcuts:
        if node_costs[shortcut] - (i + all_shortcuts[shortcut]) >= 100:
            shortcuts_by_time[node_costs[shortcut] - (i + all_shortcuts[shortcut])] += 1
            num_shortcuts += 1
print(num_shortcuts)