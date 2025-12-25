import re
import heapq
import networkx as nx


sample_input_1 = '''S2121
99925
52219
11997
3212E

S23
456
78E'''

debug = False

with open('day23.input') as f:
    input = f.read().strip().split('\n\n')
    
if debug:
    input = sample_input_1.strip().split('\n\n')
    
grids = [grid.split('\n') for grid in input]
grids = [[list(map(int, re.sub(r'[SE]', '0', line))) for line in grid] for grid in grids]

def dijkstra(grid):
    rows, cols = len(grid), len(grid[0])
    start = (0, 0)
    end = (rows - 1, cols - 1)
    
    pq = [(0, start)]
    dist = {start: 0}
        
    while pq:
        curr, (r, c) = heapq.heappop(pq)
        
        if (r, c) == end:
            return curr
        
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new = curr + grid[nr][nc]
                if (nr, nc) not in dist or new < dist[(nr, nc)]:
                    dist[(nr, nc)] = new
                    heapq.heappush(pq, (new, (nr, nc)))
                    
    return float('inf')

results = [dijkstra(grid) for grid in grids]
ans = 1
for res in results:
    ans *= res
print(ans)


def solve(grid):
    rows, cols = len(grid), len(grid[0])
    G = nx.DiGraph()
    
    source = (0, 0, 0)
    sink = (rows - 1, cols - 1, 1)
    
    for r in range(rows):
        for c in range(cols):
            if (r == 0 and c == 0) or (r == rows - 1 and c == cols - 1):
                cap = 2
            else:
                cap = 1
            G.add_edge((r,c,0), (r,c,1), capacity=cap, weight=grid[r][c])
        
            for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    G.add_edge((r,c,1), (nr,nc,0), capacity=1, weight=0)
                    
    try:
        flowDict = nx.max_flow_min_cost(G, source, sink)
        cost = nx.cost_of_flow(G, flowDict)
        return cost
    except nx.NetworkXUnfeasible:
        return float('inf')
    
results_disjoint = [solve(grid) for grid in grids]
ans_disjoint = 1
for res in results_disjoint:
    ans_disjoint *= res
print(ans_disjoint)