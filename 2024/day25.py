import aocd

lines = aocd.get_data(year=2024, day=25)
lines = [line.split('\n') for line in lines.split('\n\n')]

matches_alt = 0
for lock in lines:
    for key in lines:
        if sum([sum([1 for i in range(len(lock[0])) if lock[j][i] == '#' and key[j][i] == '#']) for j in range(len(lock))]) == 0:
            matches_alt += 1
print(matches_alt // 2)

lock_heights = [[row.count('#') - 1 for row in map(list, zip(*line))] for line in lines if line[0] == '#####']
key_heights = [[row.count('.') - 1 for row in map(list, zip(*line))] for line in lines if line[0] == '.....']
matches = 0
for i in range(len(lock_heights)):
    for j in range(len(key_heights)):
        if all(lock_heights[i][k] <= key_heights[j][k] for k in range(len(lock_heights[i]))):
            matches += 1
            
print(matches)