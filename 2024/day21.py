import aocd
import functools
import re

sample_input_1 = '''029A
980A
179A
456A
379A'''

lines = aocd.get_data(year=2024, day=21)
lines = lines.split('\n')

debug = True

if debug:
    for line in lines:
        print(line)

numpad = [['7', '8', '9'], ['4', '5', '6'], ['1', '2', '3'], ['', '0', 'A']]
dirpad = [['', '^', 'A'], ['<', 'v', '>']]

# get index of a number in the numpad
numpad_lookup = {}
for i in range(len(numpad)):
    for j in range(len(numpad[i])):
        if numpad[i][j] != '':
            numpad_lookup[numpad[i][j]] = (i, j)

dirpad_lookup = {}
for i in range(len(dirpad)):
    for j in range(len(dirpad[i])):
        if dirpad[i][j] != '':
            dirpad_lookup[dirpad[i][j]] = (i, j)

numpad_dim_order_routing = {}
dirpad_dim_order_routing = {}

'''
^> vs >^: <A>vA vs vA<^A (up > right)
^< vs <^: <Av<A vs v<<A>^A (left > up)
v< vs <v: v<A<A vs v<<A>A (left > down)
v> vs >v: v<A>A vs vA<A (down > right)
'''

for i in numpad_lookup:
    for j in numpad_lookup:
        i_row, i_col = numpad_lookup[i]
        j_row, j_col = numpad_lookup[j]
        routing = []
        if j_col == 0 and i_row == 3:
            for k in range(j_row, i_row):
                routing.append('^')
            for k in range(j_col, i_col):
                    routing.append('<')
            
        elif i_row == j_row:
            if i_col < j_col:
                for k in range(i_col, j_col):
                    routing.append('>')
            elif i_col > j_col:
                for k in range(j_col, i_col):
                    routing.append('<')
        elif j_col == i_col:
            if i_row < j_row:
                for k in range(i_row, j_row):
                    routing.append('v')
            elif i_row > j_row:
                for k in range(j_row, i_row):
                    routing.append('^')
        else: # i_row != j_row and i_col != j_col
            if i_row > j_row and i_col < j_col:
                for k in range(j_row, i_row):
                    routing.append('^')
                for k in range(i_col, j_col):
                    routing.append('>')
            elif i_row > j_row and i_col > j_col:
                for k in range(j_col, i_col):
                    routing.append('<')
                for k in range(j_row, i_row):
                    routing.append('^')
            elif i_row < j_row and i_col < j_col:
                for k in range(i_row, j_row):
                    routing.append('v')
                for k in range(i_col, j_col):
                    routing.append('>')
                
            elif i_row < j_row and i_col > j_col:
                for k in range(j_col, i_col):
                    routing.append('<')
                for k in range(i_row, j_row):
                    routing.append('v')
                
        routing.append('A')
        numpad_dim_order_routing[(i, j)] = ''.join(routing)
        
for i in dirpad_lookup:
    for j in dirpad_lookup:
        i_row, i_col = dirpad_lookup[i]
        j_row, j_col = dirpad_lookup[j]
        routing = []
        if j_row == 0 and i_col == 0:
            for k in range(i_col, j_col):
                routing.append('>')
            for k in range(j_row, i_row):
                routing.append('^')
        elif j_col == 0 and i_row == 0:
            for k in range(i_row, j_row):
                routing.append('v')
            for k in range(j_col, i_col):
                routing.append('<')
        elif i_row == j_row:
            if i_col < j_col:
                for k in range(i_col, j_col):
                    routing.append('>')
            elif i_col > j_col:
                for k in range(j_col, i_col):
                    routing.append('<')
        elif j_col == i_col:
            if i_row < j_row:
                for k in range(i_row, j_row):
                    routing.append('v')
            elif i_row > j_row:
                for k in range(j_row, i_row):
                    routing.append('^')
        else: # i_row != j_row and i_col != j_col
            if i_row > j_row and i_col < j_col:
                for k in range(j_row, i_row):
                    routing.append('^')
                for k in range(i_col, j_col):
                    routing.append('>')
            elif i_row > j_row and i_col > j_col:
                for k in range(j_col, i_col):
                    routing.append('<')
                for k in range(j_row, i_row):
                    routing.append('^')
                
            elif i_row < j_row and i_col < j_col:
                for k in range(i_row, j_row):
                    routing.append('v')
                for k in range(i_col, j_col):
                    routing.append('>')
                
            elif i_row < j_row and i_col > j_col:
                for k in range(j_col, i_col):
                    routing.append('<')
                for k in range(i_row, j_row):
                    routing.append('v')
        routing.append('A')
        dirpad_dim_order_routing[(i, j)] = ''.join(routing)

lines = ['A' + line for line in lines]

@functools.lru_cache
def get_length(str, num_machines):
    if num_machines == 0:
        return len(str)
    str = 'A' + str
    return sum([get_length(dirpad_dim_order_routing[(str[i], str[i+1])], num_machines - 1) for i in range(len(str) - 1)])


ans = 0
for line in lines[:]:
    num_seq_to_route = []
    for j in range(len(line) - 1):
        num_seq_to_route.append(numpad_dim_order_routing[(line[j], line[j+1])])
    final_string = []
    num_seq_to_route = ''.join(num_seq_to_route)
    length = get_length(num_seq_to_route, 25)
    ans += length * int(re.search(r'(\d+)', line).group(1))
    
print(ans)