import aocd
from collections import defaultdict
from collections import deque
import functools
import re
import heapq

lines = aocd.get_data(year=2024, day=17)
lines = lines.split('\n')

debug = True

if debug:
    for line in lines:
        print(line)
        
