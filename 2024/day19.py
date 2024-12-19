import aocd
import functools

lines = aocd.get_data(year=2024, day=19)
lines = lines.split('\n')

debug = False

if debug:
    for line in lines:
        print(line)

firstPartDone = False
patterns = []
designs = []

for line in lines:
    if not firstPartDone:
        if not line:
            firstPartDone = True
            continue
        else:
            patterns.append(line)
    else:
        designs.append(line)

patterns = patterns[0].split(', ')

@functools.lru_cache
def solve(design):
    ans = False
    if not design:
        return True
    for pattern in patterns:
        if design.endswith(pattern):
            ans += solve(design[:-len(pattern)])
    return ans

print(sum([solve(design) for design in designs]))