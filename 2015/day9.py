import aocd
import functools
import re

sample_input_1 = '''London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141'''

sample_input_2 = '''Faerun to Tristram = 65
Faerun to Tambi = 129
Faerun to Norrath = 144
Faerun to Snowdin = 71
Faerun to Straylight = 137
Faerun to AlphaCentauri = 3
Faerun to Arbre = 149
Tristram to Tambi = 63
Tristram to Norrath = 4
Tristram to Snowdin = 105
Tristram to Straylight = 125
Tristram to AlphaCentauri = 55
Tristram to Arbre = 14
Tambi to Norrath = 68
Tambi to Snowdin = 52
Tambi to Straylight = 65
Tambi to AlphaCentauri = 22
Tambi to Arbre = 143
Norrath to Snowdin = 8
Norrath to Straylight = 23
Norrath to AlphaCentauri = 136
Norrath to Arbre = 115
Snowdin to Straylight = 101
Snowdin to AlphaCentauri = 84
Snowdin to Arbre = 96
Straylight to AlphaCentauri = 107
Straylight to Arbre = 14
AlphaCentauri to Arbre = 46'''

# lines = aocd.get_data(year=2015, day=9)

debug = True

if not debug:
    lines = sample_input_2.split('\n')
else:
    lines = sample_input_1.split('\n')
    
# lines = lines.split('\n')
lines = [line.split() for line in lines]
forwards = [[line[0], line[2], line[4]] for line in lines]
reverses = [[line[2], line[0], line[4]] for line in lines]

forward_graph = {}


cities = list(set([line[0] for line in lines] + [line[2] for line in lines]))
cities.sort()
city_lookup = {j: i for (i,j) in enumerate(cities)}
print(cities)
print(city_lookup)
num_cities = len(cities)
one_bitmask = (1 << num_cities) - 1

if debug:
    for line in lines:
        print(line)

