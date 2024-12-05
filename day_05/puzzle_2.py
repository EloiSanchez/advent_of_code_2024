import sys

from puzzle_1 import is_correct, read_input


def sum_fixed_orders(updates, orders):
    ans = 0
    for update in updates:
        if not is_correct(update, orders):
            # print(f"fixing {update=}")
            update = fix_update(update, orders)
            # print(f"Fixed {update=}")
            ans += update[len(update) // 2]
    return ans


def fix_update(update: list[int], orders: dict[int, list], depth=0) -> list[int]:
    fixed_update = update.copy()
    if depth == 1000:
        print("max depth exceeded")
        return fixed_update
    for idx, element in enumerate(update):
        for remaining_element in update[idx + 1 :]:
            if remaining_element not in orders[element]:
                # print(
                #     f"for {element=}, {remaining_element=} not found in {orders[element]=}"
                # )
                r_idx = update.index(remaining_element)
                r_elem = fixed_update.pop(r_idx)
                fixed_update.insert(idx, r_elem)
                # print(f"new update: {fixed_update}")
                return fix_update(fixed_update, orders, depth + 1)
    return fixed_update


def main():
    orders, updates = read_input(sys.argv[1])
    answer = sum_fixed_orders(updates, orders)
    print(answer)


if __name__ == "__main__":
    main()
