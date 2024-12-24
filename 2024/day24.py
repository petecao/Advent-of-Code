import aocd
from collections import defaultdict
import functools
import re

lines = aocd.get_data(year=2024, day=24)
lines = lines.split('\n')

init_values = {}
ops = {} # output -> (op, input1, input2)

firstPartDone = False
for line in lines:
    if line == '':
        firstPartDone = True
        continue
    if not firstPartDone:
        var, val = line.split(': ')
        init_values[var] = int(val)
    else:
        lhs, output = line.split(' -> ')
        input_1, op, input_2 = lhs.split()
        ops[output] = (op, input_1, input_2)
        
actual_init_values = init_values.copy()

#swap z14 and hbk
tmp = ops['z14']
ops['z14'] = ops['hbk']
ops['hbk'] = tmp

#swap z18 and kvn
tmp = ops['z18']
ops['z18'] = ops['kvn']
ops['kvn'] = tmp

#swap z23 and dbb
tmp = ops['z23']
ops['z23'] = ops['dbb']
ops['dbb'] = tmp

#swap cvh and tfn
tmp = ops['cvh']
ops['cvh'] = ops['tfn']
ops['tfn'] = tmp

for key in sorted(ops):
    print(key, ops[key])
print()

# Part 1
@functools.lru_cache
def eval_circuit(output):
    global init_values, ops
    if output in init_values:
        return init_values[output]
    op, input_1, input_2 = ops[output]
    if op == 'AND':
        val = eval_circuit(input_1) & eval_circuit(input_2)
    elif op == 'OR':
        val = eval_circuit(input_1) | eval_circuit(input_2)
    elif op == 'XOR':
        val = eval_circuit(input_1) ^ eval_circuit(input_2)
    else:
        raise Exception('Unknown op: ' + op)
    assert val != None
    init_values[output] = val
    return val

for output in ops:
    eval_circuit(output)

ans = 0
x_input = 0
y_input = 0
relevant_wires_z = set()
relevant_wires_x = set()
relevant_wires_y = set()
for wire in sorted(init_values):
    if wire[0] == 'z':
        relevant_wires_z.add(wire)
        bit = re.findall(r'\d+', wire)[0]
        ans |= init_values[wire] << int(bit)
    if wire[0] == 'x':
        relevant_wires_x.add(wire)
        bit = re.findall(r'\d+', wire)[0]
        x_input |= init_values[wire] << int(bit)
    if wire[0] == 'y':
        relevant_wires_y.add(wire)
        bit = re.findall(r'\d+', wire)[0]
        y_input |= init_values[wire] << int(bit)
        
print(ans)

# Part 2

x_y_deps = defaultdict(set)

@functools.lru_cache
def get_x_y_deps(output):
    global x_y_deps
    if output in actual_init_values:
        x_y_deps[output] = set([output])
        return set([output])
    _, input_1, input_2 = ops[output]
    x_y_deps[output] = get_x_y_deps(input_1) | get_x_y_deps(input_2)
    return x_y_deps[output]

for wire in ops:
    get_x_y_deps(wire)

for wire in sorted(relevant_wires_z):
    print(wire, sorted(get_x_y_deps(wire), key=lambda x: int(re.findall(r'\d+', x)[0])))
    

# ans = x_input + y_input
# find incorrect bits
incorrect_bits = []

#get bits from an variable size integer
def get_bits(num):
    bits = []
    while num > 0:
        bits.append(num % 2)
        num //= 2
    return bits

ans_bits = get_bits(ans)
x_input_bits = get_bits(x_input)
y_input_bits = get_bits(y_input)
print()

print(ans_bits)
print(x_input_bits)
print(y_input_bits)

carry = 0
carry_bits = []

for i in range(len(ans_bits) - 1):
    carry_bits.append(carry)
    out_bit = x_input_bits[i] ^ y_input_bits[i] ^ carry
    if out_bit != ans_bits[i]:
        incorrect_bits.append(i)
    carry = (x_input_bits[i] & y_input_bits[i]) | (x_input_bits[i] & carry) | (y_input_bits[i] & carry)
    
if carry != ans_bits[-1]:
    incorrect_bits.append(len(ans_bits) - 1)
    
print(carry_bits)
print([i%10 for i in range(len(ans_bits))])
print(incorrect_bits)

# find the wire with the same x,y deps as z13
# bfn = c13
# dfb = x14 ^ y14
# hbk wrong, should be z14 -> hbk, z14 swap

# z18 wrong, is y18 & x18 rn
# grp = x18 ^ y18
# fgr = c17
# kvn = grp ^ fgr, wrong swap with z18

# z23 wrong, is dvw & rpg rn
# dvw = c22
# dbb = dvw ^ rpg, swap z23 with dbb
# rpg = x23 ^ y23

#z34 wrong, is mqf ^ cvh rn
# mqf= c33
# cvh wrong, is x34 & y34 rn
# tfn = x34 ^ y34, swap cvh with tfn

swapped_wires = ['hbk', 'kvn', 'dbb', 'tfn', 'cvh', 'z14', 'z18', 'z23']
print(','.join(sorted(swapped_wires)))