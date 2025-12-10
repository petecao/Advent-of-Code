import aocd
import functools
import re
from bisect import bisect_right, bisect_left

sample_input_1 = '''[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}'''

lines = aocd.get_data(year=2025, day=10)

debug = False

if not debug:
    lines = lines.split('\n')
else:
    lines = sample_input_1.split('\n')
    
# lines = lines.split('\n')

if debug:
    for line in lines:
        print(line)
        
lines = [line.split(' ') for line in lines]
final_configs = [line[0] for line in lines]
final_configs = [line.strip('[]') for line in final_configs]
for i in range(len(final_configs)):
    final_configs[i] = [0 if x == '.' else 1 for x in final_configs[i]]
buttons = [line[1:len(line)-1] for line in lines]
for i in range(len(buttons)):
    buttons[i] = [list(map(int, x.strip('()').split(','))) for x in buttons[i]]
joltages = [list(map(int, line[-1].strip('{}').split(','))) for line in lines]

starting_configs = [[0] * len(final_configs[i]) for i in range(len(final_configs))]

def bfs(starting_config, final_config, buttons):
    queue = [(starting_config, 0, [])]
    visited = set()
    while queue:
        current_config, index, path = queue.pop(0)
        if tuple(current_config) == tuple(final_config):
            return index
        if tuple(current_config) in visited:
            continue
        visited.add(tuple(current_config))
        for button in buttons:
            new_config = current_config[:]
            for j in range(len(button)):
                new_config[button[j]] = 1 - new_config[button[j]]
            queue.append((new_config, index + 1, path + [button]))
    return -1
    
print(sum([bfs(starting_configs[i], final_configs[i], buttons[i]) for i in range(len(lines))]))

from z3 import *

def lp(final_joltage, buttons):
    s = Optimize()
    counts = [Int(f'count_{i}') for i in range(len(buttons))]
    for count in counts:
        s.add(count >= 0)
    eqns = [0 for _ in range(len(final_joltage))]
    for idx, effects in enumerate(buttons):
        for effect in effects:
            eqns[effect] += counts[idx]
    for i in range(len(eqns)):
        if eqns[i] == 0:
            continue
        s.add(eqns[i] == final_joltage[i])
    total = Sum(counts)
    s.minimize(total)
    if s.check() == sat:
        m = s.model()
        return m.evaluate(total).as_long()
    return 0

print(sum([lp(joltages[i], buttons[i]) for i in range(len(lines))]))