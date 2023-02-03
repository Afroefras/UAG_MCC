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
        self.end_node = end_node

    def dijkstra(self, route: dict) -> None:
        print(route)

        new_route = {}
        winners = {}
        for sub_route, next_nodes in route.items():
            if not len(next_nodes):
                return None

            pre_winner = min(next_nodes, key=next_nodes.get)
            winners[(sub_route, pre_winner)] = next_nodes[pre_winner]
            
        winner_route, winner = min(winners, key=winners.get)
        new_sub_route = winner_route + (winner,)
        
        new_route[new_sub_route] = self.edges[(winner,)].copy()

        cum_dist = 0
        for i, _ in enumerate(new_sub_route[:-1]):
            current_node = new_sub_route[i]
            next_node = new_sub_route[i + 1]

            node_dist = self.edges[(current_node,)][next_node]
            cum_dist += node_dist

        dist_to_add = new_route[new_sub_route].items()
        new_route[new_sub_route] = {x: y + cum_dist for x, y in dist_to_add}

        route = {**route, **new_route}

        route[winner_route].pop(winner)  

        if (winner,) == self.end_node:
            print(" -> ".join(map(str, new_sub_route)))
            return None  

        self.dijkstra(route)
        


sr = ShortestRoute()
sr.read_ugly_data(data_dir="algoritmos/U3A1_Grafo_ponderado.txt")
sr.get_vars()
sr.structure_vars()
sr.create_route(start_node=(0,), end_node=(8,))

print(sr.edges)
print("\n")
# print(sr.min_route)
# print("\n")
sr.dijkstra(sr.route)
# print("\n")
# print(sr.min_route)
