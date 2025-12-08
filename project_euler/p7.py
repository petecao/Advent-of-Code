def find_nth_prime(n):
    if n == 1:
        return 2
    primes = [2]
    candidate = 3
    count = 1
    while count < n:
        is_prime = True
        sqrt_candidate = candidate ** 0.5
        for p in primes:
            if p > sqrt_candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
            count += 1
        candidate += 2  # Skip even numbers
    return primes[-1]

print(find_nth_prime(10001))