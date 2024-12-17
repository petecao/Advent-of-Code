from collections import defaultdict
import aocd

temp_input = '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47'''
lines = aocd.get_data(year=2024, day=5)
lines = lines.split('\n')
# int_lines = [[int(i) for i in line.split(',')] for line in lines]
# print(int_lines)

before_after = []
num_lists = []

firstPart = True

for line in lines:
    # print(line)
    if not line:
        firstPart = False
        continue
    if firstPart:
        before_after.append([int(i) for i in line.split('|')])
    else:
        num_lists.append([int(i) for i in line.split(',')])

priority_dict = defaultdict(list)

for i in range(len(before_after)):
    before, after = before_after[i]
    priority_dict[before].append(after)
    
sum = 0
incorrect = []
for line in num_lists:
    seen = set()
    valid = True
    for num in line:
        must_come_after = priority_dict[num]
        for i in must_come_after:
            if i in seen:
                valid = False
                break
        if not valid:
            break
        seen.add(num)
    if valid:
        # add the middle number in line to sum
        sum += line[len(line) // 2]
    else:
        incorrect.append(line)
print(sum)



sum = 0
# incorrect=[incorrect[2]]

for line in incorrect:
    attemptedFix = []
    for num in line:
        must_come_after = priority_dict[num]
        placed = False
        temp = []
        for curr in attemptedFix:
            if curr in priority_dict[num] and not placed:
                temp.append(num)
                temp.append(curr)
                placed = True
            else:
                temp.append(curr)
        if not placed:
            temp.append(num)
        attemptedFix = temp
    sum += attemptedFix[len(attemptedFix) // 2]
    
print(sum)
    