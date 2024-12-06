import sys


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")


def main():
    inp = read_input(sys.argv[1])
    print(inp)


if __name__ == "__main__":
    main()
