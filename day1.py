# get Counter
from collections import Counter
import aocd

lines = aocd.get_data(year=2024, day=1)

numbers = [[int(i) for i in line.strip().split()] for line in lines.split('\n')]

# transpost numbers
transposed = list(zip(*numbers))
list_1 = sorted(list(transposed[0]))
list_2 = sorted(list(transposed[1]))
print(sum([abs(a - b) for a, b in zip(list_1, list_2)]))

list_2_count = Counter(list_2)
ans = 0
for i in list_1:
    if list_2_count[i] > 0:
        ans += i * list_2_count[i]
print(ans)