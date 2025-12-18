from collections import defaultdict, deque
import functools
import re
import heapq

sample_input_1 = '''0 -> 3
1 -> 2
2 -> 3
3 -> 5
1 -> 3
2 -> 6
4 -> 7
'''

debug = False

with open('day17.input') as f:
    lines = f.read().strip().split('\n')
    
if debug:
    lines = sample_input_1.strip().split('\n')
    print(lines)
    
edges = [(int(re.findall(r'\d+', line)[0]), int(re.findall(r'\d+', line)[1])) for line in lines]
# print(edges)

in_deg = defaultdict(int)
graph = defaultdict(list)
reverse_graph = defaultdict(list)
for (u,v) in edges:
    graph[u].append(v)
    reverse_graph[v].append(u)
    in_deg[v] += 1
    
temp = deque([i for i in graph if in_deg[i] == 0])
q = []
while temp:
    item = temp.popleft()
    q.append(item)
    for neigh in graph[item]:
        in_deg[neigh] -= 1
        if in_deg[neigh] == 0:
            temp.append(neigh)
assert len(q) == len(set(graph.keys()).union(set(reverse_graph.keys())))

# now find longest path
dist = {i:0 for i in graph}
# print(q)
for node in q:
    # print(f'node: {node}')
    if not reverse_graph[node]:
        dist[node] = 1
        continue
    max_so_far = 0
    for pred in reverse_graph[node]:
        max_so_far = max(max_so_far, dist[pred] + 1)
    dist[node] = max_so_far
    # print(f'dist: {dist[node]}')
    
print(max(dist.values()))

# make condensation graph + SCCs
# kosaraju's algorithm
reverse_topo = q[::-1]
visited = set()
sccs = []
def dfs(node, component):
    visited.add(node)
    component.append(node)
    for neigh in graph[node]:
        if neigh not in visited:
            dfs(neigh, component)
for node in reverse_topo:
    if node not in visited:
        component = []
        dfs(node, component)
        sccs.append(component)
        
sccs_lookup = defaultdict(int)
for i,component in enumerate(sccs):
    for node in component:
        sccs_lookup[node] = i
        
condensation_graph = defaultdict(set)
reverse_condensation_graph = defaultdict(set)
for src in graph:
    for dest in graph[src]:
        src_scc = sccs_lookup[src]
        dest_scc = sccs_lookup[dest]
        if src_scc != dest_scc:
            condensation_graph[src_scc].add(dest_scc)
            reverse_condensation_graph[dest_scc].add(src_scc)
            
sources = [i for i in range(len(sccs)) if len(reverse_condensation_graph[i]) == 0]
sinks = [i for i in range(len(sccs)) if len(condensation_graph[i]) == 0]
num_sources = len(sources)
num_sinks = len(sinks)
print(f'num_sources: {num_sources}, num_sinks: {num_sinks}')
