# made on the phone on a train from Essen

import itertools
from collections import defaultdict

with open("example.txt", "r") as f:
    lines = f.read().strip().split("\n")

nodes = defaultdict(list)

rows, cols = len(lines), len(lines[0])

for i, row in enumerate(lines):
    for j, char in enumerate(row):
        if char != ".":
        	nodes[char].append((i, j))

interferences = []
for node, coords in nodes.items():
        for i, pos_0 in enumerate(coords[:-1]):
        	for pos_1 in coords[i+1:]:
        		dist = (pos_1[0] - pos_0[0], pos_1[1] - pos_0[1])
        		inf = (pos_1[0] + dist[0], pos_1[1] + dist[1])
        		if (0 <= inf[0] < rows) and (0 <= inf[1] < cols):
        			interferences.append(inf)
        
        		inf = (pos_0[0] - dist[0], pos_0[1] - dist[1])
        		if (0 <= inf[0] < rows) and (0 <= inf[1] < cols):
        			interferences.append(inf)
     
# print(nodes)   		
# print(set(interferences))
print(len(set(interferences)))