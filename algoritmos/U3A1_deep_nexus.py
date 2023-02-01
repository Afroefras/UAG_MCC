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

    def adjacency_matrix(self, is_symmetric: bool) -> None:
        self.n_nodes = len(self.nodes)
        self.adjac = zeros((self.n_nodes, self.n_nodes))

        for i, j in self.edges:
            self.adjac[i, j] = 1
            if is_symmetric:
                self.adjac[j, i] = 1

        print(self.adjac)


dn = DeepNexus()
# dn.read_ugly_data(data_dir="algoritmos/U3A1_Grafo_no_conexo.txt")
dn.read_ugly_data(data_dir="algoritmos/U3A1_test.txt")
dn.get_nodes_n_edges()
dn.adjacency_matrix(is_symmetric=True)
