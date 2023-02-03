from re import search, IGNORECASE


class ShortestRoute:
    def __init__(self) -> None:
        pass

    def read_ugly_data(self, data_dir: str) -> None:
        with open(data_dir, "r") as f:
            self.data = f.read()

    def get_nodes_n_edges(self) -> None:
        aux = r"[\S\s]*?"
        patt = rf"Nodes{aux}(\(*\d+[,\S\s]*?\)*)Edges{aux}(\[{aux}\])"
        matches = search(pattern=patt, string=self.data, flags=IGNORECASE)

        self.nodes = eval(matches.group(1))
        self.edges = eval(matches.group(2))

    def structure_vars(self) -> None:
        self.nodes = set(self.nodes)

        self.edges_dist = {}
        for node in self.nodes:
            adjac = {y: z["weight"] for x, y, z in self.edges if x == node}
            self.edges_dist[node] = adjac

    def min_dist_adjac(self, node: int) -> tuple:
        adjac = self.edges_dist[node]

        min_key = min(adjac, key=adjac.get)
        min_dist = adjac[min_key]

        return min_key, min_dist


sr = ShortestRoute()
sr.read_ugly_data(data_dir="algoritmos/U3A1_Grafo_ponderado.txt")
sr.get_nodes_n_edges()
sr.structure_vars()

print(sr.edges_dist)
print(sr.min_dist_adjac(0))
