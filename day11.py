import aocd
from collections import defaultdict
from collections import deque
import functools

sample_input = '''125 17'''

lines = aocd.get_data(year=2024, day=11)
lines = lines.split('\n')

stones = [int(i) for i in lines[0].split()]

@functools.lru_cache(maxsize=None)
def solve(stone, length):
    
    if length == 0:
        return 1
    
    if stone == 0:
        ans = solve(1, length - 1)
    elif len(str(stone)) % 2 == 0:
        half = len(str(stone)) // 2
        left = int(str(stone)[:half])
        right = int(str(stone)[half:])
        ans = solve(left, length-1) + solve(right, length-1)
    else:
        ans = solve(stone * 2024, length-1)
    
    return ans
    
    
ans = [solve(stone, 75) for stone in stones]
print(sum(ans))

