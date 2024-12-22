import aocd
from collections import defaultdict

lines = aocd.get_data(year=2024, day=22)
lines = lines.split('\n')

print(len(lines))
def get_secret_number(input, repetitions):
    prices = [input % 10]
    for _ in range(repetitions):
        tmp = input * 64
        input = (tmp ^ input) % 16777216
        tmp = int(input/32)
        input = (tmp ^ input) % 16777216
        tmp = input * 2048
        input = (tmp ^ input) % 16777216
        prices.append(input % 10)
    return input, prices

lines = [int(x) for x in lines]
ans = [get_secret_number(x, 2000) for x in lines]
print(sum([x[0] for x in ans]))
prices = [x[1] for x in ans]
changes = [[x[i] - x[i-1] for i in range(1, len(x))] for x in prices]

changes_4 = [[tuple(x[i:i+4]) for i in range(len(x)-3)] for x in changes]

set_track = defaultdict(lambda: [0] * len(lines))
seen_track = defaultdict(lambda: [False] * len(lines))

for i in range(len(changes_4)):
    for j in range(len(changes_4[i])):
        if not seen_track[changes_4[i][j]][i]:
            set_track[changes_4[i][j]][i] = prices[i][j+4]
            seen_track[changes_4[i][j]][i] = True

print(max([sum(x) for x in set_track.values()]))