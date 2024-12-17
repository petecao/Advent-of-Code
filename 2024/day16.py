import aocd
from collections import defaultdict
from collections import deque
import functools
import re
import heapq

sample_input_1 = '''###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############'''

sample_input_2 = '''#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################'''

lines = aocd.get_data(year=2024, day=16)
lines = lines.split('\n')

ccw_dirs = [(0, 1), (-1, 0), (0, -1), (1, 0)]
curr_dir = 0

debug = False
if debug:
    for line in lines:
        print(line)
        
# Part 1
sr, sc = -1, -1
er, ec = -1, -1
for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] == 'S':
            sr, sc = r, c
        if lines[r][c] == 'E':
            er, ec = r, c
            
q = []
heapq.heappush(q, (0, sr, sc, curr_dir))
shortest_length = 99999999999999999999999999999999999
parents = {(sr, sc): (0, set())}

while q:
    d, r, c, dir = heapq.heappop(q)
    if d > shortest_length:
        break
    if r == er and c == ec:
        if d < shortest_length:
            shortest_length = d
        print(d)
    if debug:
        print(d, r, c, dir)
    nr, nc = r + ccw_dirs[dir][0], c + ccw_dirs[dir][1]
    if 0 <= nr < len(lines) and 0 <= nc < len(lines[0]) and lines[nr][nc] != '#':
        if (nr, nc, dir) not in parents or d+1 < parents[(nr, nc, dir)][0]:
            parents[(nr, nc, dir)] = (d+1, set([(r, c, dir)]))
            heapq.heappush(q, (d + 1, nr, nc, dir))
        elif d+1 == parents[(nr, nc, dir)][0]:
            parents[(nr, nc, dir)][1].add((r, c, dir))
    ccw_dir = (dir + 1) % 4
    cw_dir = (dir - 1) % 4
    if (r, c, ccw_dir) not in parents or d + 1000 < parents[(r, c, ccw_dir)][0]:
        parents[(r, c, ccw_dir)] = (d + 1000, set([(r, c, dir)]))
        heapq.heappush(q, (d + 1000, r, c, ccw_dir))
    elif d + 1000 == parents[(r, c, ccw_dir)][0]:
        parents[(r, c, ccw_dir)][1].add((r, c, dir))
    if (r, c, cw_dir) not in parents or d + 1000 < parents[(r, c, cw_dir)][0]:
        parents[(r, c, cw_dir)] = (d + 1000, set([(r, c, dir)]))
        heapq.heappush(q, (d + 1000, r, c, cw_dir))
    elif d + 1000 == parents[(r, c, cw_dir)][0]:
        parents[(r, c, cw_dir)][1].add((r, c, dir))

nodes_along_shortest_path = set()
nodes_along_shortest_path.add((er, ec))
backwards_visited = set()
q = deque([i for i in parents if i[0] == er and i[1] == ec and parents[i][0] == shortest_length])
while q:
    r, c, d = q.popleft()
    if (r,c,d) in backwards_visited:
        continue
    backwards_visited.add((r,c,d))
    nodes_along_shortest_path.add((r, c))
    q.extend(parents[(r, c, d)][1])
    
print(len(nodes_along_shortest_path))