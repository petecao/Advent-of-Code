import aocd
import functools
import re

sample_input_1 = '''987654321111111
811111111111119
234234234234278
818181911112111'''

lines = aocd.get_data(year=2025, day=3)

debug = False

if not debug:
    lines = lines.split('\n')
else:
    lines = sample_input_1.split('\n')
    
# lines = lines.split('\n')

if debug:
    for line in lines:
        print(line)
        
ans = 0
for line in lines:
    max_so_far = -1
    for i in range(len(line)-1):
        tens = line[i]
        ones = max(line[i+1:])
        candidate = int(tens + ones)
        if candidate > max_so_far:
            max_so_far = candidate
    ans += max_so_far
print(ans)

ans2 = 0

for line in lines:
    # dp = 12 x len(line) -> DP[i, j] = max number ending in digit j using first i digits
    # print(len(line))
    # dp = [[-1 for _ in range(12)] for _ in range(len(line) + 1)]
    # print(len(dp))
    # print(len(dp[0]))
    # for i in dp:
    #     print(i)
    # print()
    
    # max number with i digits left to process with the first digit being j
    dp_table = [[-1 for _ in range(len(line)+1)] for _ in range(13)]
    
    
    def dp(i, j):
        if dp_table[i][j] != -1:
            return dp_table[i][j]
        
        if i == 1:
            dp_table[i][j] = int(line[j])
            return dp_table[i][j]
        
        if j == len(line) - 1:
            dp_table[i][j] = -1
            return dp_table[i][j]
        
        max_so_far = -1
        for k in range(j+1, len(line)):
            candidate = dp(i-1, k)
            if candidate > max_so_far:
                max_so_far = candidate
        if max_so_far == -1:
            dp_table[i][j] = -1
            return dp_table[i][j]
        dp_table[i][j] = int(line[j]) * 10 **(i-1) + max_so_far
        return dp_table[i][j]
            
    max_overall = -1
    max_pos = -1
    for i in range(len(line)):
        candidate = dp(12, i)
        if candidate > max_overall:
            max_overall = candidate
            max_pos = i
    # print(max_overall)
    # print(max_pos)
    ans2 += max_overall
print(ans2)