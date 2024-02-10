class Mochila:
    def __init__(self) -> None:
        pass

    def get_params(self, bag_weight: int, objects: list) -> None:
        self.initial_weight = bag_weight
        self.bag_weight = bag_weight
        self.objects = objects
        self.n_objects = len(self.objects)
        self.values, self.weights = zip(*self.objects)

        self.values = [0] + list(self.values)
        self.weights = [0] + list(self.weights)
        self.objects = [(0, 0)] + self.objects + [(0, 0)]

    def set_max_values(self) -> None:
        self.max_values = [
            ([0] * (self.bag_weight + 1)) for _ in range(self.n_objects + 1)
        ]

        for i in range(1, self.n_objects + 1):
            for j in range(1, self.bag_weight + 1):
                if j >= self.weights[i]:
                    self.max_values[i][j] = max(
                        self.max_values[i - 1][j],
                        self.max_values[i - 1][j - self.weights[i]] + self.values[i],
                    )
                else:
                    self.max_values[i][j] = self.max_values[i - 1][j]

    def choose_objects(self) -> None:
        items = [False for _ in range(self.n_objects + 2)]
        m = self.n_objects
        while m >= 1:
            i = m
            if (
                self.max_values[i][self.bag_weight]
                == self.max_values[i - 1][self.bag_weight]
            ):
                items[i] = False
            else:
                items[i] = (i, self.objects[i])
                self.bag_weight -= self.weights[i]
            m -= 1

        self.chosen = list(filter(lambda x: x, items))

    def print_result(self) -> None:
        locs, values_weights = zip(*self.chosen)
        values, weights = zip(*values_weights)

        print(f"\n{len(locs)} objects:\t\t\t{', '.join(map(str, locs))}")
        print(f"with total value of {sum(values)}:\t{', '.join(map(str, values))}")
        print(f"with weights:\t\t\t{', '.join(map(str, weights))}")
        print(f"and total weight of {sum(weights)} <= {self.initial_weight}")

    def solve(self, bag_weight, objects) -> None:
        self.get_params(bag_weight, objects)
        self.set_max_values()
        self.choose_objects()
        self.print_result()


BAG_WEIGHT = 140
OBJECTS = [
    (79, 85),
    (32, 26),
    (47, 48),
    (18, 21),
    (26, 22),
    (85, 95),
    (33, 43),
    (40, 45),
    (45, 55),
    (59, 52),
]

mch = Mochila()
mch.solve(BAG_WEIGHT, OBJECTS)
