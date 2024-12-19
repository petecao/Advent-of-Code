# get Counter
from collections import Counter
import aocd

lines = aocd.get_data(year=2015, day=1)
lines = lines.split('\n')

debug = True

if debug:
    for line in lines:
        print(line)
        
floor = 0
for j in range(len(lines[0])):
    i = lines[0][j]
    if floor == -1:
        print(j)
        break
    if i == '(':
        floor += 1
    elif i == ')':
        floor -= 1
        
print(floor)