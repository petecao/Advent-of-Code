import aocd
from collections import defaultdict
from collections import deque
import functools
import re

sample_input_1 = '''##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^'''
sample_input_2 = '''########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<'''

sample_input_3 = '''#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^'''

lines = aocd.get_data(year=2024, day=15)
lines = lines.split('\n')

debug = False

arr_to_dirs = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}

grid = []
directions = []

first_part_done = False
for line in lines:
    if line == '':
        first_part_done = True
        continue
    if not first_part_done:
        grid.append(list(line))
    else:
        directions.append(line)
        
original_grid = [row.copy() for row in grid]
        
directions = ''.join(directions)

rx, ry = -1, -1

for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] == '@':
            rx, ry = r, c
            break
        
def print_grid(grid):
    for r in grid:
        print(''.join(r))
        
if debug:
    print("Initial grid")
    print_grid(grid)
    print()
        
for arr in directions:
    if debug:
        print(arr)
    dx, dy = arr_to_dirs[arr]
    if grid[rx + dx][ry + dy] == '#':
        if debug:
            print_grid(grid)
            print('Hit a wall')
            print()
        continue
    barrels_in_row = []
    last_br, last_bc = rx, ry
    while grid[last_br + dx][last_bc + dy] == 'O':
        last_br, last_bc = last_br+dx, last_bc+dy
        barrels_in_row.append((last_br, last_bc))
        
    if barrels_in_row:
        last_barrel = barrels_in_row[-1]
        if grid[last_barrel[0] + dx][last_barrel[1] + dy] == '#':
            if debug:
                print_grid(grid)
                print('Hit a wall')
                print()
            continue
    
    for barrel in barrels_in_row:
        grid[barrel[0]+dx][barrel[1]+dy] = 'O'
    
    grid[rx][ry] = '.'
    grid[rx+dx][ry+dy] = '@'
    rx, ry = rx + dx, ry + dy
    if debug:
        print_grid(grid)
        print()

barrel_coords = []
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] == 'O':
            barrel_coords.append((r, c))
            
print(sum([100*r + c for r, c in barrel_coords]))

partTwoDebug = False
new_grid = []

if partTwoDebug:
    print("Original grid")
    print_grid(original_grid)
    print()

for row in original_grid:
    new_row = []
    for symbol in row:
        if symbol == '@':
            new_row.append('@')
            new_row.append('.')
        elif symbol == 'O':
            new_row.append('[')
            new_row.append(']')
        else:
            new_row.append(symbol)
            new_row.append(symbol)
            
    new_grid.append(new_row)
    
if partTwoDebug:
    print("New grid")
    print_grid(new_grid)
    print()
    
rx, ry = -1, -1

for r in range(len(new_grid)):
    for c in range(len(new_grid[0])):
        if new_grid[r][c] == '@':
            rx, ry = r, c
            break
        
for arr in directions[:]:
    if partTwoDebug:
        print(arr)
    dx, dy = arr_to_dirs[arr]
    if new_grid[rx + dx][ry + dy] == '#':
        if partTwoDebug:
            print_grid(new_grid)
            print('Hit a wall')
            print()
        continue
    barrels_in_row = []
    last_br, last_bc = rx, ry
    # if partTwoDebug:
    #     print (rx, ry)
    cells_to_check = deque([(rx + dx, ry + dy)])
    visited = set()
    visited.add((rx + dx, ry + dy))
    while cells_to_check:
        # if partTwoDebug:
        #     print(cells_to_check)
        r, c = cells_to_check.pop()
        # if partTwoDebug:
        #     print(new_grid[r][c])
        if new_grid[r][c] == '[':
            barrels_in_row.append(('[', r, c))
            if (r+dx, c+dy) not in visited:
                cells_to_check.append((r+dx, c+dy))
                visited.add((r+dx, c+dy))
            if (r, c+1) not in visited:
                cells_to_check.append((r, c+1))
                visited.add((r, c+1))
        elif new_grid[r][c] == ']':
            barrels_in_row.append((']', r, c))
            if (r+dx, c+dy) not in visited:
                cells_to_check.append((r+dx, c+dy))
                visited.add((r+dx, c+dy))
            if (r, c-1) not in visited:
                cells_to_check.append((r, c-1))
                visited.add((r, c-1))
        
        # if partTwoDebug:
        #     print(barrels_in_row)
        #     print()
        
    if (any([new_grid[br+dx][bc + dy] == '#' for _, br, bc in barrels_in_row])):
        if partTwoDebug:
            print_grid(new_grid)
            print('Hit a wall')
            print()
        continue
            
    # if partTwoDebug:
    #     print(barrels_in_row)
    
    for barrel in barrels_in_row:
        new_grid[barrel[1]][barrel[2]] = '.'
    
    for barrel in barrels_in_row:
        new_grid[barrel[1]+dx][barrel[2]+dy] = barrel[0]
        
    # if partTwoDebug:
    #     print_grid(new_grid)
    #     print()
    
    new_grid[rx][ry] = '.'
    new_grid[rx+dx][ry+dy] = '@'
    rx, ry = rx + dx, ry + dy
    if partTwoDebug:
        print_grid(new_grid)
        print()
    
barrel_coords = []
for r in range(len(new_grid)):
    for c in range(len(new_grid[0])):
        if new_grid[r][c] == '[':
            barrel_coords.append((r, c))
            
print(sum([100*r + c for r, c in barrel_coords]))