import aocd
import functools
import re

sample_input_1 = '''162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689'''

lines = aocd.get_data(year=2025, day=8)

debug = False

if not debug:
    lines = lines.split('\n')
else:
    lines = sample_input_1.split('\n')
    
# lines = lines.split('\n')

if debug:
    for line in lines:
        print(line)
        
class UnionFind:
    def __init__(self, points):
        self.parent = {}
        self.rank = {}
        self.connected_components = len(points)
        
    def find(self, item):
        if item not in self.parent:
            self.parent[item] = item
            self.rank[item] = 0
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]
    
    def union(self, item1, item2):
        root1 = self.find(item1)
        root2 = self.find(item2)
        
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            self.connected_components -= 1
                
def distance_squared(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return dx*dx + dy*dy + dz*dz

points = [tuple(map(int,line.split(','))) for line in lines]
uf = UnionFind(points)

edges = []
n = len(points)
for i in range(n):
    for j in range(i + 1, n):
        dist_sq = distance_squared(points[i], points[j])
        edges.append((dist_sq, i, j))
edges.sort()

def kruskals():
    ans = 0

    for _, u, v in edges[:1000]:
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            point_u = points[u]
            point_v = points[v]
            ans = point_u[0] * point_v[0]
            
    component_sizes = {}
    for point_index in range(len(points)):
        root = uf.find(point_index)
        if root not in component_sizes:
            component_sizes[root] = 0
        component_sizes[root] += 1
        
        
    largest_components = sorted(component_sizes.values(), reverse=True)[:3]
    result = 1
    for size in largest_components:
        result *= size
    print(result)
    
    for _, u, v in edges[1000:]:
        if uf.connected_components == 1:
            break
        if uf.find(u) != uf.find(v):
            uf.union(u, v)
            point_u = points[u]
            point_v = points[v]
            ans = point_u[0] * point_v[0]
    print(ans)
            
    return

kruskals()