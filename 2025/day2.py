import aocd

sample_input_1 = '''11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124'''

lines = aocd.get_data(year=2025, day=2)

debug = False

if not debug:
    lines = lines.split(',')
else:
    lines = sample_input_1.split(',')
    
lines = [tuple(line.split('-')) for line in lines]

if debug:
    for line in lines:
        print(line)
        
ans = 0
ans_sum = 0

for line in lines:
    first = line[0]
    second = line[1]
    first_len = len(first)
    second_len = len(second)
    if first_len % 2 and first_len == second_len:
        continue
    if first_len % 2:
        start = '1' + '0' * (first_len // 2)
        start = int(start * 2)
    else:
        first_half = first[:first_len // 2]
        start_candidate = first_half * 2
        if int(start_candidate) < int(first):
            start_candidate = str(int(first_half) + 1) * 2
        start = int(start_candidate)
    if second_len % 2:
        end = '9' * (second_len // 2)
        end = int(end * 2)
    else:
        second_half = second[:second_len // 2]
        end_candidate = second_half * 2
        if int(end_candidate) > int(second):
            end_candidate = str(int(second_half) - 1) * 2
        end = int(end_candidate)
    if start <= end:
        start_base = int(str(start)[:len(str(start)) // 2])
        end_base = int(str(end)[:len(str(end)) // 2])
        ans += end_base - start_base + 1
        for base in range(start_base, end_base + 1):
            long = int(str(base) * 2)
            ans_sum += long
print(ans)
print(ans_sum)

ans2 = 0
ans2_sum = 0

added = set()

for line in lines:
    first = line[0]
    second = line[1]
    first_len = len(first)
    second_len = len(second)
    for base_len in range(2, second_len + 1):
        if first_len % base_len and first_len == second_len:
            continue
        if first_len % base_len:
            start = '1' + '0' * (first_len // base_len)
            start = int(start * base_len)
        else:
            first_half = first[:first_len // base_len]
            start_candidate = first_half * base_len
            if int(start_candidate) < int(first):
                start_candidate = str(int(first_half) + 1) * base_len
            start = int(start_candidate)
        if second_len % base_len:
            end = '9' * (second_len // base_len)
            end = int(end * base_len)
        else:
            second_half = second[:second_len // base_len]
            end_candidate = second_half * base_len
            if int(end_candidate) > int(second):
                end_candidate = str(int(second_half) - 1) * base_len
            end = int(end_candidate)
        if start <= end:
            start_base = int(str(start)[:len(str(start)) // base_len])
            end_base = int(str(end)[:len(str(end)) // base_len])
            ans2 += end_base - start_base + 1
            for base in range(start_base, end_base + 1):
                long = int(str(base) * base_len)
                if long not in added:
                    ans2_sum += long
                added.add(long)
                
print(ans2)
print(ans2_sum)