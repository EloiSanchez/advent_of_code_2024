# made on the phone on a train to Essen

import itertools

with open("input.txt", "r") as f:
	lines = f.read().strip().split("\n")
	
tests = []
digits = []
for line in lines:
	test, digs = line.split(":")
	tests.append(int(test))
	digits.append([int(x) for x in digs.split()])

ans = 0
for test, digs in zip(tests, digits):
 # remove "|" for puzzle 1
	operators = ["ms|"] * (len(digs) - 1)
	for op in itertools.product(*operators):
		result = digs[0]
		for d, o in zip(digs[1:], op):
			if o == "m":
				result *= d
			elif o == "s":
				result += d
			# comment for puzzle 1
			elif o == "|":
				result = int(str(result) + str(d))
		if result == test:
			ans += result
			break

print(ans)
