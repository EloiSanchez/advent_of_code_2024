class OrderedList(list[int]):

    def add(self, new_item):
        for idx, item in enumerate(self):
            if new_item <= item:
                self.insert(idx, new_item)
                return
        self.append(new_item)


def read_input(path):
    list_1, list_2 = OrderedList(), OrderedList()
    with open(path, "r") as f:
        for line in f.readlines():
            item_1, item_2 = line.split()
            list_1.add(int(item_1))
            list_2.add(int(item_2))

    return list_1, list_2


def get_differences(list_1: OrderedList, list_2: OrderedList):
    diff = 0
    for x, y in zip(list_1, list_2):
        diff += abs(x - y)

    return diff


def main():
    list_1, list_2 = read_input("input_1.txt")
    diff = get_differences(list_1, list_2)
    print(diff)


if __name__ == "__main__":
    main()
