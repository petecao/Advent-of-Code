import aocd
import re

lines = aocd.get_data(year=2024, day=3)
lines = lines.split('\n')

print(lines)
print(len(lines))

do = True
pattern = r"\bmul\((\d+), *(\d+)\)|\b(do)\(\)|\b(don't)\(\)"
sum = 0
for line in lines:
    print(line)
    matches = re.findall(pattern, line)
    print(matches)
    for match in matches:
        if match[2] == "do":
            do = True
            continue
        elif match[3] == "don't":
            do = False
            continue
        if do:
            sum += int(match[0]) * int(match[1])
        
print(sum)