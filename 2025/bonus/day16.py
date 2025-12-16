from collections import defaultdict, deque
import functools
import re
import heapq

sample_input_1 = '''Lesson #1: Starts at t = 0 and ends at t = 20
Lesson #2: Starts at t = 50 and ends at t = 150
Lesson #3: Starts at t = 180 and ends at t = 200
Lesson #4: Starts at t = 190 and ends at t = 240 
Lesson #5: Starts at t = 10 and ends at t = 40
Lesson #6: Starts at t = 30 and ends at t = 170
Lesson #7: Starts at t = 160 and ends at t = 190
'''

debug = False

with open('day16.input') as f:
    lines = f.read().strip().split('\n')
    
if debug:
    lines = sample_input_1.strip().split('\n')
    print(lines)
    
for i in range(len(lines)):
    # temp = lines[i].split()
    # print
    # lines[i] = (temp[1][1:-1], temp[6], temp[12])
    lines[i] = tuple(map(int, re.findall(r'\d+', lines[i])))
    
print(lines)
    
lines.sort(key=lambda x: x[2])
ans = 0
last_end = -1
for i in range(len(lines)):
    start, end = lines[i][1], lines[i][2]
    if start >= last_end:
        ans += 1
        last_end = end
print(ans)

ans2 = 0
lines.sort(key=lambda x: x[1])
weeks = []
for i in range(len(lines)):
    start, end = lines[i][1], lines[i][2]
    if weeks and weeks[0] <= start:
        heapq.heappop(weeks)
    heapq.heappush(weeks, end)
print(len(weeks))