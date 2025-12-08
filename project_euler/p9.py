n = 1000

for i in range(1, n):
    for j in range(1, n - i):
        k = n - i - j
        if i * i + j * j == k * k:
            print(i * j * k)
            exit()