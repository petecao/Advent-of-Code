from collections import deque
import aocd
import functools
import re

sample_input_1 = '''3-5
10-14
16-20
12-18

1
5
8
11
17
32'''

lines = aocd.get_data(year=2025, day=5)

debug = True

if not debug:
    intervals, points = lines.split('\n\n')
else:
    intervals, points = sample_input_1.split('\n\n')
    
intervals = [list(map(int, line.split('-'))) for line in intervals.split('\n')]
points = [int(line) for line in points.split('\n')]

intervals.sort()

# Merge intervals
merged = []
for start, end in intervals:
    if not merged or merged[-1][1] < start:
        merged.append([start, end])
    else:
        merged[-1][1] = max(merged[-1][1], end)

points.sort()        
ans = 0
curr_interval_index = 0
for point in points:
    while curr_interval_index < len(merged) and merged[curr_interval_index][1] < point:
        curr_interval_index += 1
    if curr_interval_index >= len(merged):
        break
    if curr_interval_index < len(merged) and merged[curr_interval_index][0] <= point <= merged[curr_interval_index][1]:
        ans += 1
        
print(ans)

ans2 = 0
for start, end in merged:
    ans2 += (end - start + 1)
    
print(ans2)