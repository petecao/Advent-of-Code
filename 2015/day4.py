import aocd
from collections import defaultdict
from collections import deque
import functools
import re
import heapq
import hashlib

lines = aocd.get_data(year=2015, day=4)
lines = lines.split('\n')

debug = True

if debug:
    for line in lines:
        print(line)
        
key = lines[0]
i = 1
while True:
    temp_key = key + str(i)
    curr_hash = hashlib.md5(temp_key.encode()).hexdigest()
    if curr_hash[:6] == '000000':
        print(i)
        break
    i += 1