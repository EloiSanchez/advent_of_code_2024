import sys
import re
from matplotlib import pyplot as plt


def read_input(path, rows, cols):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    positions, velocities = [], []
    for line in lines:
        p = re.compile(r"p=(-{0,1}\d*),(-{0,1}\d*) v=(-{0,1}\d*),(-{0,1}\d*)")
        p1, p0, v1, v0 = (int(x) for x in p.match(line).group(1, 2, 3, 4))
        positions.append((p0, p1))
        velocities.append((v0, v1))

    return positions, velocities, int(rows), int(cols)


def safety_factor(positions: list[tuple[int, int]], rows: int, columns: int) -> int:
    q0, q1, q2, q3 = 0, 0, 0, 0
    for pos in positions:
        if (pos[0] < (rows // 2)) and (pos[1] < (columns // 2)):
            q0 += 1
        elif (pos[0] > (rows // 2)) and (pos[1] < (columns // 2)):
            q1 += 1
        elif (pos[0] < (rows // 2)) and (pos[1] > (columns // 2)):
            q2 += 1
        elif (pos[0] > (rows // 2)) and (pos[1] > (columns // 2)):
            q3 += 1
        else:
            pass
    return q0 * q1 * q2 * q3


def make_steps(
    positions: list[tuple[int, int]],
    velocities: list[tuple[int, int]],
    rows: int,
    columns: int,
    steps: int,
) -> list[tuple[int, int]]:
    new_positions = []
    for pos, vel in zip(positions, velocities):
        # We need to change from 0 based index to 1 based index for modular arithm.
        new_pos = (
            (pos[0] + steps * vel[0]) % rows,
            (pos[1] + steps * vel[1]) % columns,
        )

        new_positions.append((new_pos[0], new_pos[1]))

    return new_positions


def plot_positions(positions, rows, columns, ax):
    arr = [[0 for _ in range(columns)] for _ in range(rows)]

    for pos in positions:
        # print(pos)
        arr[pos[0]][pos[1]] = 1

    ax.imshow(arr)
    ax.set_axis_off()
    ax.autoscale(False)


def main():
    positions, velocities, rows, columns = read_input(
        sys.argv[1], sys.argv[2], sys.argv[3]
    )
    positions = make_steps(positions, velocities, rows, columns, steps=100)
    p1 = safety_factor(positions, rows, columns)
    print("p1: ", p1)

    # For P2, there is a lot of trial and error and noticing patterns. Better solutions
    # can probably be found.
    positions, velocities, rows, columns = read_input(
        sys.argv[1], sys.argv[2], sys.argv[3]
    )
    positions = make_steps(positions, velocities, rows, columns, 69)
    for i in range(1):
        fig, axs = plt.subplots(10, 10, figsize=(15, 30))
        for i in range(10 * 10):
            axs = axs.flatten()
            plot_positions(positions, rows, columns, axs[i])
            axs[i].set_title(f"{69 + i * 101}")
            positions = make_steps(positions, velocities, rows, columns, 101)

        fig.subplots_adjust(wspace=0, hspace=0.1)
        # plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
