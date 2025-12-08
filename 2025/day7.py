from collections import defaultdict, deque
import aocd


sample_input_1 = '''.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............'''

lines = aocd.get_data(year=2025, day=7)

debug = False

if not debug:
    lines = lines.split('\n')
else:
    lines = sample_input_1.split('\n')
    
if debug:
    for line in lines:
        print(line)
        
sr,sc = 0,0
for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] == 'S':
            sr, sc = r, c
            
start_r, start_c = sr, sc
splitter_map = defaultdict(list)
all_splitters = []

for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] in '^':
            splitter_map[c].append(r)
            all_splitters.append((r, c))
            
for c in splitter_map:
    splitter_map[c].sort()
    
queue = deque()
splitters_used = set()
splits_used = set()
queue.append((sr,sc))

while queue:
    r, c = queue.popleft()
    splitter_rows = splitter_map[c]
    next_splitter_row = None
    for sr in splitter_rows:
        if sr > r:
            next_splitter_row = sr
            break
    if next_splitter_row is None:
        continue
    splitters_used.add((next_splitter_row, c))
    left_c = c - 1
    right_c = c + 1
    if (next_splitter_row, left_c) not in splits_used:
        splits_used.add((next_splitter_row, left_c))
        queue.append((next_splitter_row, left_c))
    if (next_splitter_row, right_c) not in splits_used:
        splits_used.add((next_splitter_row, right_c))
        queue.append((next_splitter_row, right_c))
        
print(len(splitters_used))

paths = defaultdict(lambda: defaultdict(int))
bottom = len(lines) + 1

splitters_used = list(splitters_used)
splitters_used.sort()
splitters_by_col = defaultdict(list)
for r,c in splitters_used:
    splitters_by_col[c].append(r)

for c in splitters_by_col:
    splitters_by_col[c].sort()
    
    
first_splitter_col = start_c
first_splitter_row = None
for r in sorted(splitters_by_col[start_c]):
    if r > start_r:
        first_splitter_row = r
        break
if first_splitter_row is None:
    print(1)
    exit(0)
paths[first_splitter_row][first_splitter_col] = 1
total_paths = 0
next_rs = [0 for _ in range(len(lines[0]))]
for r,c in all_splitters:
    left_c = c - 1
    right_c = c + 1
    splitter_left_rows = splitters_by_col[left_c][next_rs[left_c]:]
    splitter_right_rows = splitters_by_col[right_c][next_rs[right_c]:]
    next_left_splitter_row = None
    next_right_splitter_row = None
    for i in range(len(splitter_left_rows)):
        sr = splitter_left_rows[i]
        if sr > r:
            next_left_splitter_row = sr
            next_rs[left_c] = i
            break
    for i in range(len(splitter_right_rows)):
        sr = splitter_right_rows[i]
        if sr > r:
            next_right_splitter_row = sr
            next_rs[right_c] = i
            break
    if next_left_splitter_row is None:
        total_paths += paths[r][c]
        paths[bottom][left_c] += paths[r][c]
    else:
        paths[next_left_splitter_row][left_c] += paths[r][c]
    if next_right_splitter_row is None:
        total_paths += paths[r][c]
        paths[bottom][right_c] += paths[r][c]
    else:
        paths[next_right_splitter_row][right_c] += paths[r][c]
print(total_paths)

# paths = defaultdict(lambda: defaultdict(int)) # paths [r][c] = number of paths to (r,c)

# total_paths = 0
# def count_paths(r, c):
#     debug2 = False
#     # print(paths)
#     if paths[r][c]:
#         if debug2:
#             print(f"Cached paths to ({r},{c}): {paths[r][c]}")
#         return paths[r][c]
#     if debug2:
#         print(f"No cached paths to ({r},{c})")
#     if r == 0:
#         if lines[r][c] == 'S':
#             return 1
#         else:
#             return 0
#     tot_paths = 0
#     splitters_in_col = splitters_by_col[c]
#     prev_splitter_row = None
#     for sr in reversed(splitters_in_col):
#         if sr < r:
#             prev_splitter_row = sr
#             break
#     if prev_splitter_row is None:
#         prev_splitter_row = -1
#     left_c = c - 1
#     right_c = c + 1

#     for sr in reversed(splitters_by_col[left_c]):
#         if sr < r and sr > prev_splitter_row:
#             if debug2:
#                 print(f"At ({r},{c}), adding paths from left splitter at ({sr},{left_c})")
#             tot_paths += count_paths(sr, left_c)
#     for sr in reversed(splitters_by_col[right_c]):
#         if sr < r and sr > prev_splitter_row:
#             if debug2:
#                 print(f"At ({r},{c}), adding paths from right splitter at ({sr},{right_c})")
#             tot_paths += count_paths(sr, right_c)
#     if start_r > prev_splitter_row and start_c == c:
#         if debug2:
#             print(f"At ({r},{c}), adding path from start at ({start_r},{start_c})")
#         tot_paths += 1
#     paths[r][c] = tot_paths
#     return tot_paths
    
# for c in range(len(lines[0])):
#     total_paths += count_paths(bottom, c)    

# print(total_paths)  

# print()
# for r in sorted(paths):
#     print(r)
#     temp = sorted([[c, paths[r][c]] for c in paths[r]])
#     print([tmp for tmp in temp if tmp[1] > 0])
#     print(sum([paths[r][c] for c in paths[r] if paths[r][c] > 0]))
#     print()