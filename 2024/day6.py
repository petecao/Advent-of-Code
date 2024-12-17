from collections import defaultdict
import aocd

sample_input = '''....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...'''

lines = aocd.get_data(year=2024, day=6)
lines = lines.split('\n')

def is_out_of_bounds(x,y):
    return x < 0 or y < 0 or x >= len(lines) or y >= len(lines[0])
    
# find the (x,y) coord of the '^' character in lines
coords = [0,0]
for i in range(len(lines)):
    for j in range(len(lines[i])):
        if lines[i][j] == '^':
            coords = [i,j]
            break
    if coords != [0,0]:
        break

dirs = [(-1,0), (0, 1), (1, 0), (0, -1)]
curr_dir = 0

visited = set()
visited.add(tuple(coords))
print(coords)

saved_coords = coords.copy()
start = coords.copy()

while True:
    x, y = dirs[curr_dir]
    if is_out_of_bounds(coords[0] + x, coords[1] + y):
        break
    if lines[coords[0] + x][coords[1] + y] == '#':
        curr_dir = (curr_dir + 1) % 4
    else:
        coords[0] += x
        coords[1] += y
        visited.add(tuple(coords))
        
print(len(visited))

visited.remove(tuple(start))

print()

coords = saved_coords
curr_dir = 0

visited_with_direction = set()
print(coords, curr_dir)

def simulate(temp_grid):
    coordinates = saved_coords.copy()
    curr_visited = set()
    current_dir = 0
    while True:
        x, y = dirs[current_dir]
        if is_out_of_bounds(coordinates[0] + x, coordinates[1] + y):
            return False
        if temp_grid[coordinates[0] + x][coordinates[1] + y] == '#':
            curr_visited.add((tuple(coordinates), current_dir))
            current_dir = (current_dir + 1) % 4
        else:
            curr_visited.add((tuple(coordinates), current_dir))
            coordinates[0] += x
            coordinates[1] += y
            if (tuple(coordinates), current_dir) in curr_visited:
                return True

ans = 0
# for coords in visited:
#     temp_lines = lines.copy()
#     for i in range(len(temp_lines)):
#         temp_lines[i] = list(temp_lines[i])
#     temp_lines[coords[0]][coords[1]] = '#'
#     if simulate(temp_lines):
#         ans += 1
# print(ans)

barriers_tested = set()
while True:
    x, y = dirs[curr_dir]
    if is_out_of_bounds(coords[0] + x, coords[1] + y):
        break
    if lines[coords[0] + x][coords[1] + y] == '#':
        visited_with_direction.add((tuple(coords), curr_dir))
        curr_dir = (curr_dir + 1) % 4
    else:
        temp_lines = lines.copy()
        for i in range(len(temp_lines)):
            temp_lines[i] = list(temp_lines[i])
        temp_visited = visited_with_direction.copy()
        if ([coords[0] + x, coords[1] + y] != start):
            temp_lines[coords[0]+x][coords[1]+y] = '#'
        saved_dir = curr_dir
        saved_x = x
        saved_y = y
        saved_coords = coords.copy()
        while True:
            if (saved_coords[0] + saved_x, saved_coords[1] + saved_y) in barriers_tested:
                break
            x, y = dirs[curr_dir]
            
            if is_out_of_bounds(coords[0] + x, coords[1] + y):
                barriers_tested.add((saved_coords[0] + saved_x, saved_coords[1] + saved_y))
                break
            if (tuple(coords), curr_dir) in temp_visited:
                # print("LOOP")
                for coords, dir in temp_visited:
                    # print(coords, dir)
                    temp_lines[coords[0]][coords[1]] = 'O'
                temp_lines[start[0]][start[1]] = '^'
                # for line in temp_lines:
                #     print(''.join(line))
                
                ans += 1
                barriers_tested.add((saved_coords[0] + saved_x, saved_coords[1] + saved_y))
                # print()
                break
            if temp_lines[coords[0] + x][coords[1] + y] == '#':
                temp_visited.add((tuple(coords), curr_dir))
                curr_dir = (curr_dir + 1) % 4
            else:
                temp_visited.add((tuple(coords), curr_dir))
                coords[0] += x
                coords[1] += y
                
        x = saved_x
        y = saved_y
        coords = saved_coords
        curr_dir = saved_dir
        visited_with_direction.add((tuple(coords), curr_dir))
        coords[0] += x
        coords[1] += y
        
        
print(ans)