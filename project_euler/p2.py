
max = 4000000
f_minus_1 = 1
f_minus_2 = 0
curr = 1

sum = 0

while curr < max:
    if curr % 2 == 0:
        sum += curr
    f_minus_2 = f_minus_1
    f_minus_1 = curr
    curr = f_minus_1 + f_minus_2
    
print(sum)