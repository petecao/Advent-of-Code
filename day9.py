import aocd
from collections import deque

sample_input = "2333133121414131402"

lines = aocd.get_data(year=2024, day=9)
lines = lines.split('\n')
line = lines[0]

even = [int(line[i]) for i in range(0, len(line), 2)]
odd = [int(line[i]) for i in range(1, len(line), 2)]
even = [(i, even[i]) for i in range(len(even))]
even = deque(even)
odd = deque(odd)
final = []
while even:
    id, freq = even.popleft()
    for i in range(freq):
        final.append(id)
    gap = 0
    tempEven = deque()
    if odd:
        gap = odd.popleft()
        while gap > 0 and even:
            rightid, rightfreq = even.pop()
            if rightfreq > gap:
                for j in range(gap):
                    final.append(rightid)
                even.append((rightid, rightfreq - gap))
                gap = 0
            else:
                for j in range(rightfreq):
                    final.append(rightid)
                gap -= rightfreq
    for j in range(gap):
        final.append(0)
    

print(sum([idx * element for idx, element in enumerate(final)]))


# PART 2

lines = aocd.get_data(year=2024, day=9)
lines = lines.split('\n')

def get_final_from_intervals(intervals):
    final = []
    for interval in intervals:
        id, start, end = interval
        if id == -1:
            id = 0
        for _ in range(start, end):
            final.append(id)
    return final

line = lines[0]


even = [int(line[i]) for i in range(0, len(line), 2)]
odd = [int(line[i]) for i in range(1, len(line), 2)]
even = [(i, even[i]) for i in range(len(even))]
even = deque(even)
odd = deque(odd)

intervals = []
idx = 0
for i in range(len(even)):
    intervals.append((even[i][0], idx, idx + even[i][1])) # exclusive
    idx += even[i][1]
    if odd:
        gap = odd.popleft()
        if gap:
            intervals.append((-1, idx, idx + gap))
            
final_intervals_right = deque()
intervals = deque(intervals)
moved_ids = set()

while intervals:
    tempLeft = deque()
    rightid, rightstart, rightend = intervals.pop()
    if rightid == -1:
        if not final_intervals_right:
            continue
        final_intervals_right.appendleft((rightid, rightstart, rightend))
        continue
    length = rightend - rightstart
    if rightid in moved_ids:
        final_intervals_right.appendleft((rightid, rightstart, rightend))
        continue
    moved = False
    moved_ids.add(rightid)
    while intervals:
        leftid, leftstart, leftend = intervals.popleft()
        if leftid != -1:
            tempLeft.append((leftid, leftstart, leftend))
            continue
        if leftend - leftstart >= length:
            tempLeft.append((rightid, leftstart, leftstart + length))
            intervals.appendleft((-1, leftstart + length, leftend))
            if final_intervals_right:
                final_intervals_right.appendleft((-1, rightstart, rightend))
            moved = True
            break
        else:
            tempLeft.append((leftid, leftstart, leftend))
    if not moved:
        final_intervals_right.appendleft((rightid, rightstart, rightend))
    
    intervals = tempLeft + intervals
    
final = get_final_from_intervals(intervals + final_intervals_right)
print(sum([idx * element for idx, element in enumerate(final)]))
