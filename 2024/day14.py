import aocd
from collections import defaultdict
from collections import deque
import functools
import re

sample_input = '''p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3'''

lines = aocd.get_data(year=2024, day=14)
lines = lines.split('\n')

debug = True

# if debug:
#     for line in lines:
#         print(line)
        
rs = 103
cs = 101

curr_p = (2,4)
v = (2, -3)

# p = r, c
is_in_q1 = lambda p: p[0] < rs // 2 and p[1] > cs // 2
is_in_q2 = lambda p: p[0] < rs // 2 and p[1] < cs // 2
is_in_q3 = lambda p: p[0] > rs // 2 and p[1] < cs // 2
is_in_q4 = lambda p: p[0] > rs // 2 and p[1] > cs // 2

def gen_graphs():
    for i in range(101*103):
        all_points = []
        count_q1 = 0
        count_q2 = 0
        count_q3 = 0
        count_q4 = 0

        for line in lines:
            c, r, vc, vr = [int(i) for i in re.findall(r'-?\d+', line)]
            curr_p = (r, c)
            v = (vr, vc)
            # print(curr_p, v)
            p_after_100_time = (curr_p[0] + i * v[0], curr_p[1] + i * v[1])
            # print(p_after_100_time)
            p_after_100_time = (p_after_100_time[0] % rs, p_after_100_time[1] % cs)
            # print(p_after_100_time)
            all_points.append(p_after_100_time)
            if is_in_q1(p_after_100_time):
                count_q1 += 1
            elif is_in_q2(p_after_100_time):
                count_q2 += 1
            elif is_in_q3(p_after_100_time):
                count_q3 += 1
            elif is_in_q4(p_after_100_time):
                count_q4 += 1
        
        a_points = set(all_points)
        visited = set()
        areas = {}
        for p in a_points:
            if p in visited:
                continue
            queue = deque([p])
            visited.add(p)
            areas[p] = 1
            while queue:
                r, c = queue.popleft()
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    new_r, new_c = r + dr, c + dc
                    if (new_r, new_c) in a_points and (new_r, new_c) not in visited:
                        visited.add((new_r, new_c))
                        queue.append((new_r, new_c))
                        areas[p] += 1
                        
        has_large_cluster = False
        for k, v in areas.items():
            if v > 100:
                has_large_cluster = True
                break
        
        if not has_large_cluster:
            continue
            
        points = [['.' for _ in range(cs)] for _ in range(rs)]
        for p in all_points:
            points[p[0]][p[1]] = '#'
            
        for row in points:
            print(''.join(row))
            
        print()
        print(i)
        
gen_graphs()