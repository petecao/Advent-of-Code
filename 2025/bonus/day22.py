from collections import defaultdict, deque
import functools
import itertools
from math import ceil, comb, floor
import re
import heapq

sample_input_1 = '''User 1:
Favorite Digit: 8
Favorite Number: 2

User 2:
Favorite Digit: 4
Favorite Number: 38

User 3:
Favorite Digit: 5
Favorite Number: 492

User 4:
Favorite Digit: 0
Favorite Number: 3'''

debug = False

with open('day22.input') as f:
    input = f.read().strip().split('\n\n')
    
if debug:
    input = sample_input_1.strip().split('\n\n')
    
input = [block.split('\n')[1:] for block in input]
for i in range(len(input)):
    fav_digit = int(input[i][0].split(': ')[1])
    fav_number = int(input[i][1].split(': ')[1])
    input[i] = (fav_digit, fav_number)
    
if debug:
    print(input)

def reconstruct_number(backpointers, state):
    num = []
    while state in backpointers:
        state, digit = backpointers[state]
        num.append(str(digit))
    num.reverse()
    return int(''.join(num))
    
def solve(digit, divisor):
    q = deque()
    visited = set()
    backpointers = {}
    # balance = freq(digit) - freq(not digit)
    
    for d in range(1, 10):
        rem = d % divisor
        balance = 1 if d == digit else -1
        
        if rem == 0 and balance >= 0:
            return d
        
        state = (rem, balance)
        if state not in visited:
            visited.add(state)
            backpointers[state] = (None, d)
            q.append(state)
            
    while q:
        rem, balance = q.popleft()
        
        for d in range(10):
            new_rem = (rem * 10 + d) % divisor
            new_balance = balance + (1 if d == digit else 0) - (1 if d != digit else 0)
            new_state = (new_rem, new_balance)
            
            if new_rem == 0 and new_balance >= 0:
                backpointers[new_state] = ((rem, balance), d)
                return reconstruct_number(backpointers, new_state)
            
            if new_state not in visited:
                visited.add(new_state)
                backpointers[new_state] = ((rem, balance), d)
                q.append(new_state)
                
ans = 0
for fav_digit, fav_number in input:
    res = solve(fav_digit, fav_number)
    if debug:
        print(fav_digit, fav_number, res)
    assert res % fav_number == 0
    assert str(res).count(str(fav_digit)) >= len(str(res)) - str(res).count(str(fav_digit))
    ans += res
    
print(ans)
    
def count_possible_m(digit, divisor):
    # dp [tot_len][remainder][number of fav digit]
    dp = [[[0 for _ in range(17)] for _ in range(divisor)] for _ in range(17)]
    for d in range(1, 10):
        rem = d % divisor
        fav_count = 1 if d == digit else 0
        dp[1][rem][fav_count] += 1
        
    for length in range(1, 16):
        for count in range(0, length + 1):
            for rem in range(divisor):
                ways = dp[length][rem][count]
                if ways == 0:
                    continue
                for d in range(10):
                    new_rem = (rem * 10 + d) % divisor
                    new_count = count + (1 if d == digit else 0)
                    dp[length + 1][new_rem][new_count] += ways
                    
    total = 0
    for length in range(8, 17):
        for count in range(ceil(length / 2), length + 1):
            total += dp[length][0][count]
    return total

ans2 = 0
for fav_digit, fav_number in input:
    res = count_possible_m(fav_digit, fav_number)
    if debug:
        print(fav_digit, fav_number, res)
    ans2 += res
print(ans2)