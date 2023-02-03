from re import search, IGNORECASE


class ShortestRoute:
    def __init__(self) -> None:
        pass

    def read_ugly_data(self, data_dir: str) -> None:
        with open(data_dir, "r") as f:
            self.data = f.read()

    def get_vars(self) -> None:
        aux = r"[\S\s]*?"
        patt = rf"Nodes{aux}(\(*\d+[,\S\s]*?\)*)Edges{aux}(\[{aux}\])"
        matches = search(pattern=patt, string=self.data, flags=IGNORECASE)

        self.raw_nodes = eval(matches.group(1))
        self.raw_edges = eval(matches.group(2))

    def structure_vars(self) -> None:
        self.nodes = set(self.raw_nodes)

        self.edges = {}
        for node in self.nodes:
            adjac = {}
            for x, y, z in self.raw_edges:
                if x == node:
                    adjac[y] = z["weight"]
            self.edges[(node,)] = adjac

    def min_dist_adjac(self, node: tuple) -> tuple:
        adjac = self.edges[node]
        winner = min(adjac, key=adjac.get)

        return (winner,)

    def add_route_distance(self, winner: tuple, route: tuple) -> None:
        new_route = route + winner
        self.edges[new_route] = self.edges[winner]

        for i, _ in enumerate(new_route[:-1]):
            current_node = new_route[i]
            next_node = new_route[i + 1]

            prev_dist = self.edges[(current_node,)][next_node]

            dist_to_add = self.edges[new_route].items()
            self.edges[new_route] = {x: y + prev_dist for x, y in dist_to_add}

    def dijkstra(self) -> None:
        pass


sr = ShortestRoute()
sr.read_ugly_data(data_dir="algoritmos/U3A1_Grafo_ponderado.txt")
sr.get_vars()
sr.structure_vars()

# a = sr.min_dist_adjac(node=(0,))
# print(a)

print(sr.edges)
print("\n")
sr.add_route_distance((5,), (0,))
print(sr.edges)
