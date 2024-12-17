import sys


class Program:

    def __init__(self, A, B, C, program) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.commands = program
        self.reset()

    def reset(self):
        self.pointer = 0
        self._output = []

    def fix(self):
        A = -1
        while self._output != self.commands:
            self.reset()
            A += 1
            self.A += A
            self.execute_program()
            if A % 100000 == 0:
                print("Doing A: ", A, "\t", end="\r")

        return A

    def execute_program(self):
        while self.pointer < len(self.commands):
            command, operand = (
                self.commands[self.pointer],
                self.commands[self.pointer + 1],
            )
            self.execute_command(command, operand)

    def execute_command(self, command, operand):
        out = None

        if command in (0, 6, 7):
            val = int(self.A / (2 ** self._parse_operand(operand)))
            if command == 0:
                self.A = val
            elif command == 6:
                self.B = val
            elif command == 7:
                self.C = val

        elif command == 1:
            self.B = self.B ^ operand

        elif command == 2:
            self.B = self._parse_operand(operand) % 8

        elif command == 3:
            if self.A != 0:
                self.pointer = operand - 2

        elif command == 4:
            self.B = self.B ^ self.C

        elif command == 5:
            out = self._parse_operand(operand) % 8
            self._output.append(out)

        self.pointer += 2

    def _parse_operand(self, operand):
        if 0 <= operand <= 3:
            return operand

        if operand == 4:
            return self.A

        if operand == 5:
            return self.B

        if operand == 6:
            return self.C

        else:
            raise ValueError(f"Wrong {operand=}")

    @property
    def output(self):
        return ",".join((str(x) for x in self._output))


def read_input(path):
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")

    A, B, C, program = 0, 0, 0, []
    for line in lines:
        if line.strip() == "":
            continue

        key, vals = line.split(":")
        if key == "Register A":
            A = int(vals)
        elif key == "Register B":
            B = int(vals)
        elif key == "Register C":
            C = int(vals)
        else:
            program = [int(x) for x in vals.split(",")]

    return A, B, C, program


def main():
    A, B, C, commands = read_input(sys.argv[1])
    program = Program(A, B, C, commands)
    program.execute_program()
    print("P1: ", program.output)
    program = Program(A, B, C, commands)
    correct_A = program.fix()
    print("\nP2: ", correct_A)


if __name__ == "__main__":
    main()
