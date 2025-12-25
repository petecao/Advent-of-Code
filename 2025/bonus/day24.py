from collections import defaultdict, deque
import functools
from math import ceil, floor
import re
import heapq
import z3

sample_input_1 = '''4 9 2 7 9 1 2 3 61 5
'''

debug = False

with open('day24.input') as f:
    lines = f.read().strip().split('\n')
    
if debug:
    lines = sample_input_1.strip().split('\n')
    print(lines)
    
assert len(lines) == 1
nums = list(map(int, lines[0].split()))

ans = 0
while len(nums) >= 1:
    new_nums = []
    ans += sum(nums)  # sum of all current numbers
    if len(nums) == 1:
        break
    for i in range(0, len(nums) - 1):
        new_nums.append(max(nums[i], nums[i + 1]) + 1)
    # if len(nums) == 2:
    #     new_nums.append(max(nums[0], nums[1]) + 1)
    nums = new_nums
    
print(ans)

nums = list(map(int, lines[0].split()))
assert len(nums) % 5 == 0
groups = []
for i in range(0, len(nums), 5):
    groups.append(nums[i:i + 5])
    
new_nums = []
for g in groups:
    init, b, c, mod, n = g
    new_nums.append(init)
    for _ in range(n - 1):
        new_nums.append((new_nums[-1] * b + c) % mod)
if debug:
    print(new_nums)
    print(1618)
    
ans = 0
    
num_elems = len(new_nums)
ans2 = num_elems * (num_elems ** 2 - 1) // 6

left = [0] * num_elems
right = [0] * num_elems
stack = []
for i in range(num_elems):
    while stack and new_nums[stack[-1]] < new_nums[i]:
        stack.pop()
    left[i] = stack[-1] if stack else -1
    stack.append(i)
    
stack = []
for i in range(num_elems - 1, -1, -1):
    while stack and new_nums[stack[-1]] <= new_nums[i]:
        stack.pop()
    right[i] = stack[-1] if stack else num_elems
    stack.append(i)
    
for i in range(num_elems):
    ans2 += new_nums[i] * (i - left[i]) * (right[i] - i)

print(ans2)