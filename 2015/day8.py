import aocd
from collections import defaultdict
from collections import deque
import functools
import re
import heapq

lines = aocd.get_data(year=2015, day=8)
lines = lines.split('\n')

debug = True

if debug:
    # for line in lines:
    #     print(line)
    print(lines[3])
    print(len(lines[3]))

ans = 0
for line in lines:
    code_len = len(line)
    memory_len = 0
    i = 1  # skip starting quote
    while i < len(line) - 1:  # skip ending quote
        if line[i] == '\\':
            if line[i + 1] == 'x':
                memory_len += 1
                i += 4
            elif line[i + 1] in ['\\', '"']:
                memory_len += 1
                i += 2
        else:
            memory_len += 1
            i += 1
    ans += code_len - memory_len
print(ans)    

ans2 = 0
for line in lines:
    code_len = len(line)
    encoded_len = 2  # for starting and ending quotes
    for char in line:
        if char in ['\\', '"']:
            encoded_len += 2
        else:
            encoded_len += 1
    ans2 += encoded_len - code_len
print(ans2)