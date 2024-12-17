from collections import defaultdict
import aocd

sample_input = '''190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20'''

lines = aocd.get_data(year=2024, day=7)
lines = lines.split('\n')

split_lines = [line.split(': ') for line in lines]
results = [int(line[0]) for line in split_lines]
operands = [[int(x) for x in line[1].split(' ')] for line in split_lines]
ans = 0
for i in range(len(results)):
    queue = [] # contains tuple(remaining_operands, current_number)
    curr_list = operands[i]
    curr_operand = curr_list[0]
    queue.append((curr_list[1:], curr_operand))
    found = False
    while queue:
        curr_trial = queue.pop()
        if not curr_trial[0]:
            if curr_trial[1] == results[i]:
                found = True
                break
            else:
                continue
        else:
            if curr_operand > results[i]:
                continue
            curr_operand = curr_trial[0][0]
            queue.append((curr_trial[0][1:], curr_trial[1] + curr_operand))
            queue.append((curr_trial[0][1:], curr_trial[1] * curr_operand))
            queue.append((curr_trial[0][1:], curr_trial[1] * (10 ** len(str(curr_operand))) + curr_operand))
    if found:
        ans += results[i]
print(ans)