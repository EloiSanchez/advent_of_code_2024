from collections import defaultdict
import sys
from puzzle_1 import read_input, decompress, get_checksum


def parse_input(characters):
    parsed = defaultdict(list)
    blocks = []
    for idx, length in enumerate(characters):
        if idx % 2 == 0:
            id = idx // 2
        else:
            id = "."
        blocks.append([id, int(length)])
    blocks.append([".", 0])
    return blocks


def reorder(blocks: list[list], depth=0):
    idx, r_idx = 0, len(blocks) - 1
    id = 0
    # changed = False

    # if depth >= 2:
    #     print(f"depht={depth}")
    #     return blocks
    while r_idx > 0:
        r_id, r_length = r_block = blocks[r_idx]
        r_idx -= 1
        # print("doing block", r_block)
        if r_id != ".":
            for idx, block in enumerate(blocks):
                id, length = block
                if idx >= r_idx:
                    break
                if id == ".":
                    # print("checking", idx, block, r_idx, r_block)
                    if r_length <= length:
                        # print("Correct, changing...")
                        # print_block(blocks)
                        blocks.pop(r_idx + 1)
                        blocks.insert(idx, r_block)
                        # r_idx += 1
                        # blocks.insert(idx, [".", 0])
                        # blocks[r_idx + 1][1] = blocks[r_idx + 1][1] + r_length
                        # print(f"{new_length=}")
                        blocks[idx + 1][1] = blocks[idx + 1][1] - r_length
                        if blocks[r_idx + 2][0] == ".":
                            blocks[r_idx + 2][1] = blocks[r_idx + 2][1] + r_length
                        else:
                            blocks.insert(r_idx + 1, [".", r_length])
                        # print_block(blocks)
                        break
    #     print("done block", r_block)
    # print("finished", blocks)
    # merged = []
    # for idx, block_0 in enumerate(blocks):
    #     if block_0[0] != ".":
    #         merged.append(block_0.copy())
    #     else:
    #         if merged[-1][0] == ".":
    #     merged[-1][1] += block_0[1]
    # else:
    #     merged.append(block_0.copy())
    # print("mergeddd", merged)

    # if changed:
    #     return reorder(merged, depth + 1)
    # return merged
    return blocks


def print_block(blocks):
    char = ""
    for id, length in blocks:
        for _ in range(length):
            char += str(id)
    print(char)


def get_checksum(reordered):
    idx = 0
    checksum = 0
    for id, length in reordered:
        if id == ".":
            # print(f"{idx=}, {id=}")
            idx += length
        else:
            for _ in range(length):
                # print(f"{idx=}, {id=}")
                checksum += idx * id
                idx += 1
    return checksum


def main():
    inp = read_input(sys.argv[1])
    # print(inp)
    blocks = parse_input(inp)
    # print(blocks)
    reordered = reorder(blocks)
    # print(reordered)
    checksum = get_checksum(reordered)
    print(checksum)


if __name__ == "__main__":
    main()
