from numpy import zeros
from re import search, IGNORECASE


class ShortestRoute:
    def __init__(self) -> None:
        pass

    def read_ugly_data(self, data_dir: str) -> None:
        with open(data_dir, "r") as f:
            self.data = f.read()

    def get_nodes_n_edges(self) -> None:
        aux = r"[\S\s]*?"
        patt = rf"Nodes{aux}(\d+[,\S\s]*?)Edges{aux}(\[{aux}\])"
        matches = search(pattern=patt, string=self.data, flags=IGNORECASE)

        self.nodes = eval(matches.group(1))
        self.edges = eval(matches.group(2))

        self.nodes = set(self.nodes)
        self.edges = {(x[0], x[1]): x[2]["weight"] for x in self.edges}

    def distance_matrix(self) -> None:
        self.max_distance = max(self.edges.values())

        self.edges_rev = {
            x: -(y - self.max_distance - 1) for x, y in self.edges.items()
        }

        self.n_nodes = len(self.nodes)
        self.dist = zeros((self.n_nodes, self.n_nodes))

        for i, j in self.edges_rev.keys():
            self.dist[i, j] = self.edges_rev[(i, j)]

    def get_adjancency_edges(self, node: int) -> set:
        node_row = self.dist[node, :].copy()
        adjac_nodes = filter(lambda x: node_row[x] > 0, range(self.n_nodes))
        return set(adjac_nodes)

        


sr = ShortestRoute()
sr.read_ugly_data(data_dir="algoritmos/U3A1_Grafo_ponderado.txt")
sr.get_nodes_n_edges()

sr.distance_matrix()
