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

    def create_route(self, start_node: tuple) -> None:
        self.route = {start_node: self.edges[start_node]}
        
    def dijkstra(self, min_route: dict) -> None:
        print(min_route)

        new_min_route = {}
        winners = {}
        for route, next_nodes in min_route.items():
            if not len(next_nodes):
                return None

            pre_winner = min(next_nodes, key=next_nodes.get)
            winners[(route, pre_winner)] = next_nodes[pre_winner]
            
        winner_route, winner = min(winners, key=winners.get)
        new_route = winner_route + (winner,)
        
        print(winner_route, '->', winner, ':', winners[(winner_route, winner)])
        print(self.edges[(winner,)])

        new_min_route[new_route] = self.edges[(winner,)]

        for i, _ in enumerate(new_route[:-1]):
            current_node = new_route[i]
            next_node = new_route[i + 1]

            prev_dist = self.edges[(current_node,)][next_node]

            dist_to_add = new_min_route[new_route].items()
            new_min_route[new_route] = {x: y + prev_dist for x, y in dist_to_add}

        min_route = {**min_route, **new_min_route}

        min_route[winner_route][winner] = 100        
        self.dijkstra(min_route)
        


sr = ShortestRoute()
sr.read_ugly_data(data_dir="algoritmos/U3A1_Grafo_ponderado.txt")
sr.get_vars()
sr.structure_vars()
sr.create_route(start_node=(0,))

print(sr.edges)
print("\n")
# print(sr.min_route)
# print("\n")
sr.dijkstra(sr.route)
# print("\n")
# print(sr.min_route)
