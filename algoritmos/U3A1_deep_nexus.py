from numpy import zeros
from re import search, IGNORECASE


class DeepNexus:
    def __init__(self) -> None:
        pass

    def read_ugly_data(self, data_dir: str) -> None:
        with open(data_dir, "r") as f:
            self.data = f.read()

    def get_nodes_n_edges(self) -> None:
        aux = r"[\S\s]*?"
        patt = rf"Nodes{aux}(\({aux}\)){aux}Edges{aux}(\[{aux}\])"
        matches = search(pattern=patt, string=self.data, flags=IGNORECASE)

        self.nodes = eval(matches.group(1))
        self.edges = eval(matches.group(2))

    def adjacency_matrix(self) -> None:
        self.n_nodes = len(self.nodes)
        self.adjac = zeros((self.n_nodes, self.n_nodes))

        for i, j in self.edges:
            self.adjac[i, j] = 1
            self.adjac[j, i] = 1

    def create_discovered_nodes(self) -> None:
        self.disc_nodes = set()

    def get_adjancency_edges(self, node: int) -> set:
        node_row = self.adjac[node, :].copy()
        adjac_nodes = filter(lambda x: node_row[x] == 1, range(self.n_nodes))
        return set(adjac_nodes)

    def deep_search(self, node: int) -> None:
        self.disc_nodes.add(node)
        for node_end in self.get_adjancency_edges(node):
            if node_end not in self.disc_nodes:
                print(f"{str(node).zfill(2)} -> {str(node_end).zfill(2)}")
                self.deep_search(node_end)

    def deep_search_all(self) -> None:
        i = 0
        while len(self.disc_nodes) < self.n_nodes:
            i += 1
            print(f"\nSubgraph #{i}:")

            nodes_left = set(self.nodes) - self.disc_nodes
            node = next(iter(nodes_left))
            
            self.deep_search(node)


dn = DeepNexus()
dn.read_ugly_data(data_dir="algoritmos/U3A1_Grafo_no_conexo.txt")

dn.get_nodes_n_edges()
dn.adjacency_matrix()
dn.create_discovered_nodes()

dn.deep_search_all()
