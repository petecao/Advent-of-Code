from collections import defaultdict, deque
import functools
import re
import heapq
import bisect
import sys

sample_input_1 = '''Pattern:
101101?
1??????
??110?1
00???00

String:
1011011

'''
sys.setrecursionlimit(70000)
debug = False

with open('day18.input') as f:
    lines = f.read().strip().split('\n\n')
    

    
if debug:
    lines = sample_input_1.strip().split('\n\n')
    print(lines)
    

patterns = lines[0].split('\n')[1:]
patterns = [list(line) for line in patterns]
string = lines[1].split('\n')[-1]
string = list(string)
if debug:
    print(patterns)
    print(string)

count = 0
for i in patterns:
    flag = True
    for j in range(len(string)):
        if not (i[j] == '?' or i[j] == string[j]):
            flag = False
            break
    if flag:
        count += 1
print(count)

# flatten patterns
pattern = [c for patt in patterns for c in patt]
# print(pattern)

pattern_len = len(pattern)
string_len = len(string)
start_locs = []
for i in range(pattern_len - string_len + 1):
    window = pattern[i: i + string_len]
    if all(s == '?' or s == t for s, t in zip(window, string)):
        start_locs.append(i)

good_shifts = set()
start_locs_set = set(start_locs)
for shift in range(1, string_len):
    good = True
    for i in range(string_len - shift):
        if string[i] != string[i+shift]:
            good = False
            break
    if good:
        good_shifts.add(shift)
        
skip_all_lookup = []
for i in start_locs:
    next = bisect.bisect_left(start_locs, i + string_len)
    skip_all_lookup.append(next)
        
# dp_must_take[i] = max matches given that we start at take i
# dp_must_take[i] = max(1 + dp_must_take[next_good_shift], dp_can_skip[next_skip_all])
# dp_can_skip[i] = max matches given that we can skip i
# dp_can_skip[i] = max(dp_can_skip[i+1], dp_must_take[i])
memo_must_take = defaultdict(int)
memo_can_skip = defaultdict(int)

def dp_must_take(idx):
    if idx == len(start_locs):
        return 0
    if memo_must_take[idx]:
        return memo_must_take[idx]
    val = start_locs[idx]
    max_take = 0
    for shift in good_shifts:
        if val + shift not in start_locs_set:
            continue
        new_idx = bisect.bisect_left(start_locs, val + shift)
        if new_idx < len(start_locs):
            max_take = max(max_take, dp_must_take(new_idx))
    skip_all_idx = skip_all_lookup[idx]
    if (skip_all_idx < len(start_locs)):
        max_take = max(max_take, dp_can_skip(skip_all_idx))
    max_take += 1
    memo_must_take[idx] = max_take
    return memo_must_take[idx]

def dp_can_skip(idx):
    if idx == len(start_locs):
        return 0
    if memo_can_skip[idx]:
        return memo_can_skip[idx]
    ignore = dp_can_skip(idx+1)
    memo_can_skip[idx] = max(ignore, dp_must_take(idx))
    return memo_can_skip[idx]
    
print(dp_can_skip(0))