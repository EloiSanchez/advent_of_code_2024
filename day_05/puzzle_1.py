import sys
from typing import DefaultDict


def read_input(path):
    orders, updates = DefaultDict(list), []

    with open(path, "r") as f:
        phase = 1

        for line in f.readlines():
            if phase == 1:
                vals = line.split("|")
                if len(vals) != 2:
                    phase += 1
                    continue
                orders[int(vals[0])].append(int(vals[1]))

            elif phase == 2:
                updates.append([int(x) for x in line.split(",")])

    return orders, updates


def is_correct(update: list[int], orders: dict[int, list]):
    for idx, element in enumerate(update):
        for remaining_element in update[idx + 1 :]:
            if not remaining_element in orders[element]:
                return False
    return True


def sum_correct_orders(updates, orders):
    ans = 0
    for update in updates:
        if is_correct(update, orders):
            ans += update[len(update) // 2]
    return ans


def main():
    orders, updates = read_input(sys.argv[1])
    answer = sum_correct_orders(updates, orders)
    print(answer)


if __name__ == "__main__":
    main()
