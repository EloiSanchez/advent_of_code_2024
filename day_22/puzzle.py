from collections import defaultdict, deque
import sys


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    return [int(x) for x in lines]


def generate_secret_number(num: int) -> int:
    def mix(x, y):
        return x ^ y

    def prune(x):
        return x % 16777216

    num = prune(mix(num, num * 64))
    num = prune(mix(num, int(num / 32)))
    return prune(mix(num, num * 2048))


def generate_nth_number(number: int, steps: int):
    price_0 = int(str(number)[-1])
    sequences = defaultdict(lambda: 0)
    seq = deque()

    for _ in range(steps):
        # Get new number
        number = generate_secret_number(number)

        # Build up sequences and prices
        price = int(str(number)[-1])
        seq.append(price - price_0)
        if len(seq) > 4:
            seq.popleft()
            if tuple(seq) not in sequences:
                sequences[tuple(seq)] = price
        price_0 = price

    return sequences, number


def get_best_nth_sequence(starts: list[int], steps: int) -> tuple[int, int]:
    p1 = 0
    all_sequences = set()
    all_prices = []

    # Find price sequences final numbers
    for start in starts:
        prices, number = generate_nth_number(start, steps)
        all_sequences = all_sequences.union(prices.keys())
        all_prices.append(prices)
        p1 += number

    # Find best sequence
    p2 = 0
    for sequence in all_sequences:
        seq_price = 0
        for prices in all_prices:
            seq_price += prices[sequence]
        if seq_price > p2:
            p2 = seq_price

    return p1, p2


def main():
    numbers = read_input(sys.argv[1])
    p1, p2 = get_best_nth_sequence(numbers, 2000)
    print("P1: ", p1, "P2: ", p2)


if __name__ == "__main__":
    main()
