import aocd
from collections import defaultdict

lines = aocd.get_data(year=2024, day=23)
lines = lines.split('\n')
        
edges = [line.split('-') for line in lines]

adj_list = defaultdict(list)
for edge in edges:
    adj_list[edge[0]].append(edge[1])
    adj_list[edge[1]].append(edge[0])

triangles = set()

for edge in edges:
    for neighbor in adj_list[edge[0]]:
        if neighbor in adj_list[edge[1]]:
            triangles.add(tuple(sorted([edge[0], edge[1], neighbor])))
            
ans = 0
for triangle in triangles:
    if any(node[0] == 't' for node in triangle):
        ans += 1
print(ans)

# Part 2: find max clique
max_clique = set()
def find_max_clique(clique, nodes):
    global max_clique
    if not nodes:
        if len(clique) > len(max_clique):
            max_clique = clique
    for v in nodes.copy():
        find_max_clique(clique.union({v}), nodes.intersection(adj_list[v]))
        nodes.remove(v)
        
find_max_clique(set(), set(adj_list.keys()))
print(','.join(sorted(max_clique)))