from collections import defaultdict
import functools
import re

sample_input_1 = '''plant 5
spray even
spray odd
plant 9
spray all
plant 4
spray even
'''

debug = False

# get lines from day13.input
with open('day13.input') as f:
    lines = f.read().strip().split('\n')
    
if debug:
    lines = sample_input_1.strip().split('\n')
    print(lines)
    
instructions = [line.split() for line in lines]

ans = 0
even_count = 0
odd_count = 0
for instr in instructions:
    if instr[0] == 'plant':
        num = int(instr[1])
        if num % 2 == 0:
            even_count += 1
        else:
            odd_count += 1
        ans += num
    else:
        if instr[1] == 'even':
            ans += even_count
            odd_count += even_count
            even_count = 0
        elif instr[1] == 'odd':
            ans += odd_count
            even_count += odd_count
            odd_count = 0
        else:
            ans += even_count + odd_count
            odd_count, even_count = even_count, odd_count
print(ans)

counts = defaultdict(int)
for instr in instructions:
    if instr[0] == 'plant':
        num = int(instr[1])
        counts[num] += 1
    else:
        new_counts = defaultdict(int)
        if instr[1] == 'even':
            for k, v in counts.items():
                if k % 2 == 0:
                    new_counts[k // 2] += v
                else:
                    new_counts[k] += v
        elif instr[1] == 'odd':
            for k, v in counts.items():
                if k % 2 == 1:
                    new_counts[k // 2] += v
                else:
                    new_counts[k] += v
        else:
            for k, v in counts.items():
                new_counts[k // 2] += v
        counts = new_counts
ans2 = sum([k * v for k, v in counts.items()])
print(ans2)
            