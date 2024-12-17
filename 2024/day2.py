import aocd

lines = aocd.get_data(year=2024, day=2)
lines = lines.split('\n')
lines = [line.split() for line in lines]
# make every element in the nested list an integer
lines = [[int(i) for i in line] for line in lines]


ans = 0
for line in lines:
    # get every sublist where 1 element is removed
    # check if each line is monotonically increasing or decreasing
    all_sublists = [line[:i] + line[i+1:] for i in range(len(line))]
    tot_flag = False
    for sublist in all_sublists:
        if len(set(sublist)) != len(sublist):
            continue
        if sublist == sorted(sublist) or sublist == sorted(sublist, reverse=True):
            flag = True
            for i in range(1, len(sublist)):
                if abs(sublist[i] - sublist[i-1]) > 3:
                    flag = False
                    break
            if flag:
                tot_flag = True
        if tot_flag:
            break
    if tot_flag:
        ans += 1

print(ans)