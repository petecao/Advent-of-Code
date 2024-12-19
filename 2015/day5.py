import aocd
from collections import defaultdict
from collections import deque
import functools
import re
import heapq

lines = aocd.get_data(year=2015, day=5)
lines = lines.split('\n')

debug = True

if debug:
    for line in lines:
        print(line)
        
vowels = 'aeiou'
forbidden = ['ab', 'cd', 'pq', 'xy']

# lines = ['ugknbfddgicrmopn', 'aaa', 'jchzalrnumimnmhp', 'haegwjzuvuyypxyu', 'dvszwmarrgswjxmb']

ans = 0
for line in lines:
    print(line)
    has_vowel = (sum([c in vowels for c in line]) >= 3)
    print(has_vowel)
    has_forbidden = any([s in line for s in forbidden])
    print(has_forbidden)
    has_double = any([line[i] == line[i+1] for i in range(len(line)-1)])
    print(has_double)
    if has_vowel and not has_forbidden and has_double:
        ans += 1
        
print(ans)

ans2 = 0
for line in lines:
    has_double = any([line[i:i+2] in line[i+2:] for i in range(len(line)-1)])
    has_pair = any([line[i] == line[i+2] for i in range(len(line)-2)])
    if has_double and has_pair:
        ans2 += 1
        
print(ans2)
    