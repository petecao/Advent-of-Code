import aocd
import functools
import re

sample_input_1 = '''L68
L30
R48
L5
R60
L55
L1
L99
R14
L82'''

lines = aocd.get_data(year=2025, day=1)

debug = False

if not debug:
    lines = lines.split('\n')
else:
    lines = sample_input_1.split('\n')

if debug:
    for line in lines:
        print(line)
        
start = 50

positions = []

position = start
for line in lines:
    dir = line[0]
    steps = int(line[1:])
    if dir == 'L':
        position -= steps
    else:
        position += steps
    position = position % 100
    positions.append(position)

print(len([_ for _ in positions if _ == 0]))

positions = start
num_times_passed_zero = 0
for line in lines:
    dir = line[0]
    steps = int(line[1:])
    old_position = positions
    if dir == 'L':
        remaining_to_zero = (positions - 0) % 100
        if steps >= remaining_to_zero:
            num_times_passed_zero += 1
            num_times_passed_zero += (steps - remaining_to_zero - 1) // 100
        positions -= steps
    else:
        remaining_to_zero = (100 - positions) % 100
        if steps >= remaining_to_zero:
            num_times_passed_zero += 1
            num_times_passed_zero += (steps - remaining_to_zero - 1) // 100
        positions += steps

    positions = positions % 100
        
print(num_times_passed_zero)