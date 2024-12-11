import sys


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip()
    return lines.split()


def blink_stones(stones, steps):
    stones = [blink(stone, steps) for stone in stones]
    return sum(stones)


# Create cache
cache = {}


def blink(stone, steps):
    # If stone/step combination found in cache return it
    if (stone, steps) in cache:
        return cache[(stone, steps)]

    # Else, calculate it
    if steps == 0:
        value = 1
    elif stone == "0":
        value = blink("1", steps - 1)
    elif (len_stone := len(stone)) % 2 == 0:
        value = blink(stone[: len_stone // 2], steps - 1) + blink(
            str(int(stone[len_stone // 2 :])), steps - 1
        )
    else:
        value = blink(str(int(stone) * 2024), steps - 1)

    # Save newly calculated value into cache
    cache[(stone, steps)] = value

    return value


def main():
    stones = read_input(sys.argv[1])
    p1 = blink_stones(stones, 25)
    p2 = blink_stones(stones, 75)
    print(f"{p1=}, {p2=}")


if __name__ == "__main__":
    main()
