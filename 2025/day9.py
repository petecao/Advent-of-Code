import aocd
import functools
import re
from bisect import bisect_right, bisect_left

sample_input_1 = '''7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3'''

lines = aocd.get_data(year=2025, day=9)

debug = False

if not debug:
    lines = lines.split('\n')
else:
    lines = sample_input_1.split('\n')
    
# lines = lines.split('\n')

if debug:
    for line in lines:
        print(line)
        
def rect_area(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x1 - x2)+1) * (abs(y1 - y2)+1)

ans = -1
points = [tuple(map(int,line.split(','))) for line in lines]
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        area = rect_area(points[i], points[j])
        if area > ans:
            ans = area
print(ans)

horizontal_edges = []
vertical_edges = []
for i in range(len(points)):
    x1, y1 = points[i]
    x2, y2 = points[(i+1) % len(points)]
    if y1 == y2:
        if x1 > x2:
            x1, x2 = x2, x1
        horizontal_edges.append((y1, x1, x2))
    else:
        if y1 > y2:
            y1, y2 = y2, y1
        vertical_edges.append((x1, y1, y2))
        
horizontal_edges.sort()
vertical_edges.sort()

def rect_in_poly(p1, p2, h_edges, v_edges):
    rx_min, rx_max = min(p1[0], p2[0]), max(p1[0], p2[0])
    ry_min, ry_max = min(p1[1], p2[1]), max(p1[1], p2[1])
    eps = 0.0001
    v1 = (rx_min + eps, ry_min + eps)
    v2 = (rx_min + eps, ry_max - eps)
    v3 = (rx_max - eps, ry_max - eps)
    v4 = (rx_max - eps, ry_min + eps)
    
    vs = [v1, v2, v3, v4]
    vs_intersect_to_inf = [[x for (x, y1, y2) in v_edges if y1 < v[1] < y2 and x > v[0]] for v in vs]
    # edges = p1->p2 (left vertical), p2->p3 (top horizontal), p3->p4 (right vertical), p4->p1 (bottom horizontal)    
    
    if any(len(lst) % 2 == 0 for lst in vs_intersect_to_inf):
        return False
    
    vertical_x1 = [x for (x, y1, y2) in v_edges if y1 < ry_min and y2 > ry_min and rx_min < x < rx_max] # v4->v1
    vertical_x2 = [x for (x, y1, y2) in v_edges if y1 < ry_max and y2 > ry_max and rx_min < x < rx_max] # v2->v3
    horizontal_y1 = [y for (y, x1, x2) in h_edges if x1 < rx_min and x2 > rx_min and ry_min < y < ry_max] # v1->v2
    horizontal_y2 = [y for (y, x1, x2) in h_edges if x1 < rx_max and x2 > rx_max and ry_min < y < ry_max] # v3->v4
    lens = [len(vertical_x1), len(vertical_x2), len(horizontal_y1), len(horizontal_y2)]
    if any(lens):
        return False
    return True
    
ans2 = -1
for i in range(len(points)):
    for j in range(i + 1, len(points)):
        area = rect_area(points[i], points[j])
        if area > ans2:
            if rect_in_poly(points[i], points[j], horizontal_edges, vertical_edges):
                # print("FOUND")
                # print(points[i], points[j])
                ans2 = area
print(ans2)
