from collections import defaultdict
import aocd
import functools
import re
from bisect import bisect_right, bisect_left

sample_input_1 = '''aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out'''

sample_input_2 = '''svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out'''


lines = aocd.get_data(year=2025, day=11)

debug = False

if not debug:
    lines = lines.split('\n')
else:
    lines = sample_input_2.split('\n')
    
if debug:
    for line in lines:
        print(line)
        
lines = [line.split(': ') for line in lines]
lines = {line[0]: line[1].split(' ') for line in lines}

counts = defaultdict(int)
def count_paths_to_out(node, destination='out'):
    # print(node, destination, counts)
    if node == destination:
        return 1
    if node in counts:
        return counts[node]
    count = 0
    if node not in lines:
        return 0
    for next_node in lines[node]:
        count += count_paths_to_out(next_node, destination)
    counts[node] = count
    return count
print(count_paths_to_out('you'))

prod = 1
for source, dest in [['svr', 'dac'], ['dac', 'fft'], ['fft', 'out']]:
    counts = defaultdict(int)
    prod *= count_paths_to_out(source, dest)
prod2 = 1
for source, dest in [['svr', 'fft'], ['fft', 'dac'], ['dac', 'out']]:
    counts = defaultdict(int)
    prod2 *= count_paths_to_out(source, dest)
print(prod+prod2)