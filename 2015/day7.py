import aocd
from collections import defaultdict
from collections import deque
import functools
import re
import heapq

lines = aocd.get_data(year=2015, day=7)
lines = lines.split('\n')

debug = False

if debug:
    for line in lines:
        print(line)
        
split_lines = [line.split(' ') for line in lines]
# (instrs, outputs) = zip(*[(line[:-2], line[-1]) for line in split_lines])
instrs = {}
for line in split_lines:
    instrs[line[-1]] = line[:-2]
    
values = {}
values['b'] = 3176  # for part 2

def solve(x):
    if x in values:
        return values[x]
    if x.isdigit():
        return int(x)
    instr = instrs[x]
    if len(instr) == 1:
        try:
            val = int(instr[0])
        except:
            val = solve(instr[0])
    elif len(instr) == 2:
        val = ~solve(instr[1]) & 0xFFFF
    else:
        left = solve(instr[0])
        op = instr[1]
        right = solve(instr[2])
        if op == 'AND':
            val = left & right
        elif op == 'OR':
            val = left | right
        elif op == 'LSHIFT':
            val = (left << right) & 0xFFFF
        elif op == 'RSHIFT':
            val = left >> right
    values[x] = val
    return val

print(solve('a'))