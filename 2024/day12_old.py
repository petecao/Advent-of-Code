import aocd
from collections import defaultdict
from collections import deque
import functools

sample_input_1 = '''AAAA
BBCD
BBCC
EEEC'''

sample_input_2 = '''OOOOO
OXOXO
OOOOO
OXOXO
OOOOO'''

sample_input_3 = '''RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE'''

sample_input_4 = '''EEEEE
EXXXX
EEEEE
EXXXX
EEEEE'''

sample_input_5 = '''AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA'''

lines = aocd.get_data(year=2024, day=12)
lines = lines.split('\n')
    
def is_in_bounds(r,c):
    return 0 <= r < len(lines) and 0 <= c < len(lines[0])
    
areas = defaultdict(int)
perimeters = defaultdict(int)
up_borders = defaultdict(set)
down_borders = defaultdict(set)
left_borders = defaultdict(set)
right_borders = defaultdict(set)
visited = set()

for r in range(len(lines)):
    for c in range(len(lines[0])):
        if (r, c) in visited:
            continue
        # print(lines[r][c])
        queue = deque([(r, c)])
        visited.add((r, c))
        areas[(r,c)] = 1
        while queue:
            row, col = queue.popleft()
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row, new_col = row + dr, col + dc
                if is_in_bounds(new_row, new_col) and lines[new_row][new_col] == lines[row][col]:
                    if (new_row, new_col) in visited:
                        continue
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col))
                    areas[(r,c)] += 1
                else:
                    if (dr, dc) == (0, 1):
                        right_borders[(r,c)].add((new_row, new_col))
                        if (row + 1, new_col) not in right_borders[(r,c)] and (row - 1, new_col) not in right_borders[(r,c)]:
                            perimeters[(r,c)] += 1
                    elif (dr, dc) == (0, -1):
                        left_borders[(r,c)].add((new_row, new_col))
                        if (row + 1, new_col) not in left_borders[(r,c)] and (row - 1, new_col) not in left_borders[(r,c)]:
                            perimeters[(r,c)] += 1
                    elif (dr, dc) == (1, 0):
                        down_borders[(r,c)].add((new_row, new_col))
                        if (new_row, col + 1) not in down_borders[(r,c)] and (new_row, col - 1) not in down_borders[(r,c)]:
                            perimeters[(r,c)] += 1
                    else:
                        up_borders[(r,c)].add((new_row, new_col))
                        if (new_row, col + 1) not in up_borders[(r,c)] and (new_row, col - 1) not in up_borders[(r,c)]:
                            perimeters[(r,c)] += 1
                                
assert len(areas) == len(perimeters)
print(sum([areas[k] * perimeters[k] for k in areas.keys()]))