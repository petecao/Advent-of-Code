from math import floor
import aocd
from collections import defaultdict
from collections import deque
import functools
import re

sample_input_1 = '''Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0'''

lines = aocd.get_data(year=2024, day=17)
lines = lines.split('\n')

debug = True

if debug:
    for line in lines:
        print(line)
        
# a, b, c = ints from first 3 lines
a = int(lines[0].split()[-1])
b = int(lines[1].split()[-1])
c = int(lines[2].split()[-1])

numbers = [int(i) for i in lines[-1].split()[-1].split(',')]
# pair up consecutive numbers in numbers
instructions = [(numbers[i], numbers[i+1]) for i in range(0, len(numbers), 2)]

if debug:
    print(a, b, c)
    print(instructions)

def get_combo_operand(operand):
    if operand in range(4):
        return operand
    elif operand == 4:
        return a
    elif operand == 5:
        return b
    elif operand == 6:
        return c
    else:
        assert False

pc = 0
output = []

while pc < len(instructions):
    opcode = instructions[pc][0]
    operand = instructions[pc][1]
    
    if opcode == 0:
        a = a /(2 ** get_combo_operand(operand))
        a = int(floor(a))
    elif opcode == 1:
        b ^= operand
    elif opcode == 2:
        b = get_combo_operand(operand) % 8
    elif opcode == 3:
        if a != 0:
            pc = operand
            continue
    elif opcode == 4:
        b ^= c
    elif opcode == 5:
        output.append(get_combo_operand(operand) % 8)
    elif opcode == 6:
        b = a /(2 ** get_combo_operand(operand))
        b = int(floor(b))
    elif opcode == 7:
        c = a/ (2 ** get_combo_operand(operand))
        c = int(floor(c))
    else:
        assert False
    pc += 1
    
print(','.join([str(i) for i in output]))

queue = deque()
queue.append((0, []))
candidates = []

while queue:
    curr, results = queue.pop()
    if results == numbers:
        candidates.append(curr)
    for i in range(8):
        a = curr * 8 + i
        b = 0
        c = 0
        pc = 0
        output = []
        while pc < len(instructions):
            opcode = instructions[pc][0]
            operand = instructions[pc][1]
            
            if opcode == 0:
                a = a /(2 ** get_combo_operand(operand))
                a = int(floor(a))
            elif opcode == 1:
                b ^= operand
            elif opcode == 2:
                b = get_combo_operand(operand) % 8
            elif opcode == 3:
                if a != 0:
                    pc = operand
                    continue
            elif opcode == 4:
                b ^= c
            elif opcode == 5:
                output.append(get_combo_operand(operand) % 8)
            elif opcode == 6:
                b = a /(2 ** get_combo_operand(operand))
                b = int(floor(b))
            elif opcode == 7:
                c = a/ (2 ** get_combo_operand(operand))
                c = int(floor(c))
            else:
                assert False
            pc += 1
        if output == numbers[-(len(results)+1):]:
            queue.append((curr * 8 + i, output))

print()
print(min(candidates))