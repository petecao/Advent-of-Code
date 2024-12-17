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
borders = defaultdict(set)
sides = defaultdict(int)
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
                        borders[(r,c)].add((new_row, col + 0.25))
                    elif (dr, dc) == (0, -1):
                        borders[(r,c)].add((new_row, col - 0.25))
                    elif (dr, dc) == (1, 0):
                        borders[(r,c)].add((row + 0.25, new_col))
                    else:
                        borders[(r,c)].add((row - 0.25, new_col))


def find_num_sides_from_border_segments(shape_borders): # shape borders is a set of border segments
    num_sides = 0
    visited = set()
    for border in shape_borders:
        if border in visited:
            continue
        num_sides += 1
        if type(border[0]) == int:
            # vertical border
            queue = deque([border])
            while queue:
                row, col = queue.popleft()
                for dr, dc in [(1, 0), (-1, 0)]:
                    new_row, new_col = row + dr, col
                    if (new_row, new_col) in shape_borders and (new_row, new_col) not in visited:
                        visited.add((new_row, new_col))
                        queue.append((new_row, new_col))
        else:
            # horizontal border
            queue = deque([border])
            while queue:
                row, col = queue.popleft()
                for dr, dc in [(0, 1), (0, -1)]:
                    new_row, new_col = row, col + dc
                    if (new_row, new_col) in shape_borders and (new_row, new_col) not in visited:
                        visited.add((new_row, new_col))
                        queue.append((new_row, new_col))
            
    return num_sides

for k in areas.keys():
    sides[k] = find_num_sides_from_border_segments(borders[k])
    
print(sum([areas[k] * sides[k] for k in areas.keys()]))