from collections import defaultdict, deque
import functools
import re

sample_input_1 = '''INP: abc
abc: def ghi
def: OUT ghi
ghi: OUT BIN
'''

debug = False

# get lines from day13.input
with open('day14.input') as f:
    lines = f.read().strip().split('\n')
    
if debug:
    lines = sample_input_1.strip().split('\n')
    # print(lines)
    
N = 12**3456
if debug:
    N = 6
    
graph = {line.split(':')[0]:line.split(':')[1].split() for line in lines}
freq = defaultdict(int)

assert len(graph['INP']) == 1

in_deg = defaultdict(int)
for i in graph:
    for j in graph[i]:
        in_deg[j] += 1

temp = deque([i for i in graph if in_deg[i] == 0])
q = []

while temp:
    item = temp.popleft()
    q.append(item)
    if item not in graph:
        continue
    for neigh in graph[item]:
        in_deg[neigh] -= 1
        if in_deg[neigh] == 0:
            temp.append(neigh)

freq['INP'] = N

for item in q:
    if item not in graph:
        continue
    curr_freq = freq[item]
    neighs = graph[item]
    
    if len(neighs) == 1:
        freq[neighs[0]] += curr_freq
    else:
        freq[neighs[0]] += (curr_freq + 1) // 2
        freq[neighs[1]] += curr_freq // 2
    
# print(freq)
print(freq['OUT'] % 10**15)
