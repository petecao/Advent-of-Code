n = 999

sum = 0

for i in range(1, n // 3 + 1):
    sum += i * 3
    
for i in range(1, n // 5 + 1):
    sum += i * 5
    
for i in range(1, n // 15 + 1):
    sum -= i * 15
    
print(sum)