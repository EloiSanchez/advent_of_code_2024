def read_input(path):
    lines = []
    with open(path, "r") as f:
        for line in f.readlines():
            parsed_line = [int(x) for x in line.split()]
            lines.append(parsed_line)
    return lines


def count_safe(lines: list[list[int]]):
    safe_count = 0
    for line in lines:
        # print(line)
        safe = is_safe(line)
        safe_count += 1 if safe else 0

    return safe_count


def is_safe(line):
    monotony = None
    safe = True
    for idx, x in enumerate(line[1:]):
        x_0 = line[idx]
        if monotony == "asc" and x <= x_0:
            # print(f"{x_0} / {x} not asc")
            safe = False
            break
        elif monotony == "desc" and x >= x_0:
            # print(f"{x_0} / {x} not desc")
            safe = False
            break
        elif not (1 <= abs(x - x_0) <= 3):
            # print(f"{x_0} / {x} bad increment")
            safe = False
            break
        elif monotony is None:
            if x > x_0:
                # print(f"{x_0} / {x} setting asc")
                monotony = "asc"
            elif x < x_0:
                # print(f"{x_0} / {x} setting desc")
                monotony = "desc"
            else:
                # print(f"{x_0} / {x} cannot set monotony")
                safe = False
                break
    # print(safe)
    return safe


def main():
    lines = read_input("input.txt")
    safe_count = count_safe(lines)
    print(safe_count)


if __name__ == "__main__":
    main()
