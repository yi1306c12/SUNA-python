#!/usr/env/bin python3
import networkx as nx


class novelty_map(nx.Graph):
    def __init__(self,max_population):
        self.max_population = max_population
        super().__init__()

    def append(self,new):
        new_distances = [new.distance(n) for n in self.nodes()]
        if len(self) < self.max_population:
            self.add_node(new)
            self.add_weighted_edges_from([(new,n,dist) for n,dist in zip(self.nodes(),new_distances)])#zip() iterates shortest times


if __name__ == '__main__':
    class test_gene(int):
        def distance(self,other):
            return 0
    nm = novelty_map(10)
    nm.append(test_gene(1))
    nm.append(test_gene(2))
    nm.append(test_gene(3))

    pos = nx.shell_layout(nm)
    nx.draw_networkx_nodes(nm,pos)
    nx.draw_networkx_edges(nm,pos)
    nx.draw_networkx_edge_labels(nm,pos)
    import matplotlib.pyplot as plt
    plt.show()
