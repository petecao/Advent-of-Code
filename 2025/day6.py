import aocd
from itertools import zip_longest

sample_input_1 = '''123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  '''

lines = aocd.get_data(year=2025, day=6)

debug = False

if not debug:
    lines = lines.split('\n')
else:
    lines = sample_input_1.split('\n')
    
lines_unsplit = lines
lines = [line.strip().split() for line in lines]
lines_transposed = list(zip(*lines))

ans = 0
for line in lines_transposed:
    op = line[-1]
    numbers = list(map(int, line[:-1]))
    if op == '*':
        prod = 1
        for num in numbers:
            prod *= num
        ans += prod
    elif op == '+':
        ans += sum(numbers)
print(ans)

transposed_lines_with_reversed_ops = [[list(i[::-1]) for i in line] for line in lines_transposed]

for line in transposed_lines_with_reversed_ops:
    op = line[-1]
    numbers = list(zip_longest(*line[:-1], fillvalue=''))
    numbers = [int(''.join(num).strip()) for num in numbers]
    
    
unsplit_lines_list = [list(line) for line in lines_unsplit]
cols = list(zip_longest(*unsplit_lines_list, fillvalue=''))[::-1]
numbers = [col[:-1] for col in cols]
ops = [col[-1] for col in cols]
numbers = [''.join(num).strip() for num in numbers]

ans2 = 0
curr_operands = []

for i in range(len(ops)):
    curr_num = numbers[i]
    if curr_num:
        curr_operands.append(int(curr_num))
    curr_op = ops[i]
    if curr_op == '*':
        prod = 1
        for num in curr_operands:
            prod *= num
        ans2 += prod
        curr_operands = []
    elif curr_op == '+':
        ans2 += sum(curr_operands)
        curr_operands = []
print(ans2)