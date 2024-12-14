import sys
import re


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    machines = []
    for i in range(0, len(lines), 4):
        l1, l2, l3, *_ = lines[i : i + 4]
        buttons = re.compile(r".*X\+(\d*).*\+(\d*)")
        buttons = re.compile(r".*X\+(\d*).*\+(\d*)")
        prizes = re.compile(r".*X=(\d*).*Y=(\d*)")

        button_a = tuple(map(int, buttons.match(l1).group(1, 2)))
        button_b = tuple(map(int, buttons.match(l2).group(1, 2)))
        prize = tuple(map(int, prizes.match(l3).group(1, 2)))
        machines.append([button_a, button_b, prize])
    return machines


def calculate_prices(
    machines: list[list[tuple[int, int]]], add_to_price: int | None = None
):
    price = 0
    for machine in machines:
        # Get result of solving machine
        result = solve_machine(machine, add_to_price)

        # If there is a solution, calculate price
        if result:
            price += 3 * result[0] + result[1]

    return price


def solve_machine(machine: list[tuple], add_to_price: int | None) -> tuple | None:
    """
    Equation to solve is:

    a0 * i + b0 * j = p0 |
                         | -> Which in matrix form is A * X = P
    a1 * i + b1 * j = p1 |

    And has analytical solution for as:

    X = (1 / det A) * A^(-1) * P
    """
    a, b, prize = machine

    if add_to_price is not None:
        prize = (prize[0] + add_to_price, prize[1] + add_to_price)

    det = a[0] * b[1] - b[0] * a[1]
    if det == 0:
        return None

    i = prize[0] * b[1] - prize[1] * b[0]
    j = prize[1] * a[0] - prize[0] * a[1]

    if (i % det == 0) and (j % det == 0):
        return int(i / det), int(j / det)

    return None


def main():
    machines = read_input(sys.argv[1])
    p1 = calculate_prices(machines)
    p2 = calculate_prices(machines, add_to_price=10000000000000)
    print("p1: ", p1, "p2: ", p2)


if __name__ == "__main__":
    main()
