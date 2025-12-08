max_pal = 0
for i in range(999, 99, -1):
    for j in range(i, 99, -1):
        product = i * j
        if product <= max_pal:
            break
        if str(product) == str(product)[::-1]:
            max_pal = product
print(max_pal)