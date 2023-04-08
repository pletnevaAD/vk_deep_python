class CustomList(list):
    def __add__(self, other):
        new_list = CustomList(
            map(sum, zip([*self, *[0] * (len(other) - len(self))], [*other, *[0] * (len(self) - len(other))])))
        return new_list

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        new_list = CustomList(map(lambda tuple_xy: tuple_xy[0] - tuple_xy[1],
                                  zip([*self, *[0] * (len(other) - len(self))],
                                      [*other, *[0] * (len(self) - len(other))])))
        return new_list

    def __rsub__(self, other):
        new_list = CustomList(map(lambda tuple_xy: tuple_xy[1] - tuple_xy[0],
                                  zip([*self, *[0] * (len(other) - len(self))],
                                      [*other, *[0] * (len(self) - len(other))])))
        return new_list

    def __str__(self):
        return f"Список: {super().__str__()}\nСумма элементов списка: {sum(self)}"

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)
