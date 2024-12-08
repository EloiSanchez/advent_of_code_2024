# made on the phone on a train from Essen

import itertools
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().strip().split("\n")

nodes = defaultdict(list)

rows, cols = len(lines), len(lines[0])

for i, row in enumerate(lines):
    for j, char in enumerate(row):
        if char != ".":
        	nodes[char].append((i, j))

interferences = []
for node, coords in nodes.items():
    for i, pos_0 in enumerate(coords):
        print(node, pos_0)
        for j, pos_1 in enumerate(coords):
            if i == j:
        	    continue
            dist = (pos_1[0] - pos_0[0], pos_1[1] - pos_0[1])
            k = 0
            inf = pos_0
            while (0 <= inf[0] < rows) and (0 <= inf[1] < cols):
        	    interferences.append(inf)
        	    k+=1
        	    inf = (pos_0[0] + k * dist[0], pos_0[1] + k * dist[1])

     
# print(nodes)   		
# print(set(interferences))
print(len(set(interferences)))