from numpy import inf
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

    def create_route(self, start_node: tuple, end_node: tuple) -> None:
        self.route = {start_node: self.edges[start_node].copy()}
        self.start_node = start_node
        self.end_node = end_node

    def dijkstra(self, route: dict) -> None:
        new_routes = {}
        winners = {}
        for new_sub_route, next_nodes in route.items():
            if not len(next_nodes):
                return None

            pre_winner = min(next_nodes, key=next_nodes.get)
            winners[(new_sub_route, pre_winner)] = next_nodes[pre_winner]

        winner_route, winner = min(winners, key=winners.get)
        sub_route = winner_route + (winner,)

        cum_dist = [0]
        for i, _ in enumerate(sub_route[:-1]):
            current_node = sub_route[i]
            next_node = sub_route[i + 1]

            node_dist = self.edges[(current_node,)][next_node]
            cum_dist.append(node_dist)

        new_routes[sub_route] = self.edges[(winner,)].copy()

        sum_dist = sum(cum_dist)
        dist_to_add = new_routes[sub_route].items()

        new_routes[sub_route] = {x: y + sum_dist for x, y in dist_to_add}
        route = {**route, **new_routes}

        if (winner,) == self.end_node:
            full_route = zip(map(str, sub_route), cum_dist)
            full_route_dist = [f'"{x}" ({y})' for x, y in full_route]
            full_route_dist = " -> ".join(full_route_dist)

        route[winner_route].pop(winner)
        self.dijkstra(route)


sr = ShortestRoute()
sr.read_ugly_data(data_dir="algoritmos/U3A1_Grafo_ponderado.txt")
sr.get_vars()
sr.structure_vars()
sr.create_route(start_node=(0,), end_node=(14,))

print(sr.edges)
print("\n")
# print(sr.min_route)
# print("\n")
sr.dijkstra(sr.route)
# print("\n")
# print(sr.min_route)
