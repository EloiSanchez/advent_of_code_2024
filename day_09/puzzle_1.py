import sys


def read_input(path):
    with open(path, "r") as f:
        line = f.read().strip()
    return line


def decompress(line):
    decompressed = []
    for idx, char in enumerate(line):
        for _ in range(int(char)):
            if idx % 2 == 0:
                decompressed.append(idx // 2)
            else:
                decompressed.append(".")
    return decompressed


def reorder(elements: list):
    reordered = []
    N = len(elements)
    idx = 0
    bckw_idx = -1

    while idx <= (N + bckw_idx):
        elem = elements[idx]
        idx += 1
        if elem == ".":
            find_backwards = True
            while find_backwards:
                replacement = elements[bckw_idx]
                bckw_idx -= 1
                if replacement != ".":
                    reordered.append(replacement)
                    find_backwards = False
        else:
            reordered.append(elem)
    return reordered


def get_checksum(reordered):
    ans = 0
    for idx, elem in enumerate(reordered):
        if elem != ".":
            ans += idx * elem
    return ans


def main():
    inp = read_input(sys.argv[1])
    # print(inp)
    decompressed = decompress(inp)
    print("".join([str(x) for x in decompressed]))
    reordered = reorder(decompressed)
    print("".join([str(x) for x in reordered]))
    checksum = get_checksum(reordered)
    print(checksum)


if __name__ == "__main__":
    main()
