n = 600851475143

if n % 2 == 0:
    while n % 2 == 0:
        n = n // 2
    if n == 1:
        print(2)
        exit()

i = 3
while i * i <= n:
    while n % i == 0:
        n = n // i
    i += 2

print(n)