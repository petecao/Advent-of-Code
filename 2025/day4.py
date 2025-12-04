from collections import deque
import aocd
import functools
import re

sample_input_1 = '''..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.'''

lines = aocd.get_data(year=2025, day=4)

debug = False

if not debug:
    lines = lines.split('\n')
else:
    lines = sample_input_1.split('\n')
    
def is_in_bounds(r,c):
    return 0 <= r < len(lines) and 0 <= c < len(lines[0])
        
dirs = [(-1,0),(1,0),(0,-1),(0,1), (-1,-1),(-1,1),(1,-1),(1,1)]

ans = 0

q = deque()

for r in range(len(lines)):
    for c in range(len(lines[0])):
        if lines[r][c] == '@':
            count = 0
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if is_in_bounds(nr, nc) and lines[nr][nc] == '@':
                    count += 1
            if count < 4:
                ans += 1
                q.append((r,c))
print(ans)

ans2 = 0
changed = True
lines = [list(row) for row in lines]
# while changed:
#     changed = False
#     removable = []
#     for r in range(len(lines)):
#         for c in range(len(lines[0])):
#             if lines[r][c] == '@':
#                 count = 0
#                 for dr, dc in dirs:
#                     nr, nc = r + dr, c + dc
#                     if is_in_bounds(nr, nc) and lines[nr][nc] == '@':
#                         count += 1
#                 # print(f"Cell ({r}, {c}) has {count} neighboring '@' cells.")
#                 if count < 4:
#                     ans2 += 1
#                     removable.append((r,c))
#                     changed = True  
#     for r, c in removable:
#         lines[r][c] = '.'

while q:
    r, c = q.popleft()
    if lines[r][c] == '.':
        continue
    lines[r][c] = '.'
    ans2 += 1
    for dr, dc in dirs:
        nr, nc = r + dr, c + dc
        if is_in_bounds(nr, nc) and lines[nr][nc] == '@':
            count = 0
            for ddr, ddc in dirs:
                nnr, nnc = nr + ddr, nc + ddc
                if is_in_bounds(nnr, nnc) and lines[nnr][nnc] == '@':
                    count += 1
            if count < 4:
                q.append((nr,nc))
    
print(ans2)