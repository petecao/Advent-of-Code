from collections import defaultdict, deque
import functools
from math import ceil, floor
import re
import heapq
import z3

sample_input_1 = '''(4, 6) r=3
(3, 7) r=1
(12, 14) r=9
(10, 6) r=5
'''

debug = False

with open('day20.input') as f:
    lines = f.read().strip().split('\n')
    
if debug:
    lines = sample_input_1.strip().split('\n')
    print(lines)
    
sensors = []
radii = []
for line in lines:
    parts = line.split(' ')
    # line in form (x, y) r=R
    x = int(parts[0][1:-1])
    y = int(parts[1][:-1])
    r = int(parts[2][2:])
    sensors.append((x, y))
    radii.append(r)
if debug:
    print(sensors)
    print(radii)
    
intersect_counts = defaultdict(int)
intersects = defaultdict(list)
for i in range(len(sensors)):
    (x1, y1) = sensors[i]
    r1 = radii[i]
    for j in range(i + 1, len(sensors)):
        (x2, y2) = sensors[j]
        r2 = radii[j]
        dist_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2
        radius_sum = r1 + r2
        if dist_sq**0.5 < radius_sum:
            intersect_counts[i] += 1
            intersect_counts[j] += 1
            intersects[i].append(j)
            intersects[j].append(i)
            
max_intersects = -1
best_sensor_idx = -1
for sensor_idx in intersect_counts:
    if intersect_counts[sensor_idx] > max_intersects:
        max_intersects = intersect_counts[sensor_idx]
        best_sensor_idx = sensor_idx
        
best_pos = sensors[best_sensor_idx]
best_radius = radii[best_sensor_idx]
print(best_pos[0], best_pos[1], best_radius)
print(best_pos[0] * best_pos[1] + intersect_counts[best_sensor_idx])
if debug:
    print(intersect_counts)
    
# part 2: find the point that is in range of the most sensors
# use z3 to solve this

minx = min([s[0] - r for (s, r) in zip(sensors, radii)])
maxx = max([s[0] + r for (s, r) in zip(sensors, radii)])
miny = min([s[1] - r for (s, r) in zip(sensors, radii)])
maxy = max([s[1] + r for (s, r) in zip(sensors, radii)])
print(minx, maxx, miny, maxy)

def circle_intersections(x1, y1, r1, x2, y2, r2):
    d = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    if d < abs(r1 - r2):
        return []

    a = (r1**2 - r2**2 + d**2) / (2 * d)
    h = (r1**2 - a**2)**0.5
    x0 = x1 + a * (x2 - x1) / d
    y0 = y1 + a * (y2 - y1) / d
    rx = -(y2 - y1) * (h / d)
    ry = (x2 - x1) * (h / d)

    p1 = (x0 + rx, y0 + ry)
    p2 = (x0 - rx, y0 - ry)

    return [p1, p2]

candidate_points = set()
for i in range(len(sensors)):
    for j in intersects[i]:
        (x1, y1) = sensors[i]
        r1 = radii[i]
        (x2, y2) = sensors[j]
        r2 = radii[j]
        pts = circle_intersections(x1, y1, r1, x2, y2, r2)
        if not pts:
            candidate_points.add((x1, y1))
            candidate_points.add((x2, y2))
        for (px, py) in pts:
            candidate_points.add((floor(px), floor(py)))
            candidate_points.add((floor(px), ceil(py)))
            candidate_points.add((ceil(px), floor(py)))
            candidate_points.add((ceil(px), ceil(py)))
            
max_covered = -1
best_point = None
for (px, py) in candidate_points:
    covered_count = 0
    for i in range(len(sensors)):
        (sx, sy) = sensors[i]
        r = radii[i]
        dist_sq = (px - sx) ** 2 + (py - sy) ** 2
        if dist_sq < r * r:
            covered_count += 1
    if covered_count > max_covered:
        max_covered = covered_count
        best_point = (px, py)
        
print(best_point[0], best_point[1], max_covered)
print(best_point[0] * best_point[1])

