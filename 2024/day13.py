import aocd
import re

lines = aocd.get_data(year=2024, day=13)
lines = lines.split('\n')
        
lines = [i for i in lines if i]

ans = 0

for i in range(0, len(lines), 3):
    machine_a = lines[i]
    machine_b = lines[i+1]
    tot = lines[i+2]
    
    a_x, a_y = [int(i) for i in re.findall(r'\d+', machine_a)]
    b_x, b_y = [int(i) for i in re.findall(r'\d+', machine_b)]
    x, y = [10000000000000+int(i) for i in re.findall(r'\d+', tot)]
    
    denom = a_x * b_y - a_y * b_x
    assert denom != 0
    a = (x * b_y - y * b_x) / denom
    b = (a_x * y - x * a_y) / denom
    
    if a == int(a) and b == int(b):
        ans += (3 * a + b)
        
print(ans)