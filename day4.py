import aocd

def is_out_of_bounds(x,y):
    return x < 0 or y < 0 or x >= len(lines) or y >= len(lines[0])

lines = aocd.get_data(year=2024, day=4)
lines = lines.split('\n')
# for line in lines:
    # print(line)
    # print(len(line))

print(len(lines))
print(len(lines[0]))

three_steps = [[(0,0), (0,1), (0,2), (0,3)],
               [(0,0), (0, -1), (0, -2), (0, -3)],
               [(0,0), (1,0), (2,0), (3,0)],
               [(0,0), (-1,0), (-2,0), (-3,0)],
               [(0,0), (1,1), (2,2), (3,3)],
               [(0,0), (-1,-1), (-2,-2), (-3,-3)],
               [(0,0), (1,-1), (2,-2), (3,-3)],
               [(0,0), (-1,1), (-2,2), (-3,3)]]

XMAS = ['X', 'M', 'A', 'S']

count = 0

for i in range(len(lines)):
    for j in range(len(lines[0])):
        if lines[i][j] == 'X':
            for sequence in three_steps:
                for step in sequence:
                    x, y = step
                    if is_out_of_bounds(i + x, j + y):
                        break
                    if lines[i + x][j + y] != XMAS[sequence.index(step)]:
                        break
                else:
                    count += 1

print(count)

four_steps = [[(0,0), (0,2), (1, 1), (2, 0), (2,2)],
              [(0,0), (2,0), (1, 1), (0, 2), (2,2)],
              [(0,0), (0,2), (-1, 1), (-2,0), (-2,2)],
              [(0,0), (2,0), (1, -1), (0, -2), (2,-2)]]

count = 0
MMASS = ['M', 'M', 'A', 'S', 'S']

for i in range(len(lines)):
    for j in range(len(lines[0])):
        if lines[i][j] == 'M':
            for sequence in four_steps:
                for step in sequence:
                    x, y = step
                    if is_out_of_bounds(i + x, j + y):
                        break
                    if lines[i + x][j + y] != MMASS[sequence.index(step)]:
                        break
                else:
                    count += 1
                    
print(count)