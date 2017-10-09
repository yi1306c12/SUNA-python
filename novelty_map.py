import networkx as nx

def argmin(l):
    return l.index(min(l))


def get_edge_distance(edge):
    return edge[2]['weight']


class novelty_map(nx.Graph):
    
    def __init__(self,max_size):
        assert max_size > 0, "novelty_map size must be > 0"
        self.max_size = max_size
        super().__init__()
    
    def add_node(self, new_node):
        assert hasattr(new_node, 'distance'), "node must be able to calculate distance to an other"

        current_nodes = list(self.nodes())
        new_node_distances = [new_node.distance(n) for n in current_nodes]

        #if map is not full
        if len(current_nodes) < self.max_size:
            super().add_node(new_node)
            self.add_weighted_edges_from([(new_node, n, dist) for n,dist in zip(current_nodes, new_node_distances)])
            return True

        #else if worst_node closer than new_node
        current_min_edge = self.get_minimum_edge()      
        if get_edge_distance(current_min_edge) < min(new_node_distances):
            worst_node = self.get_worse_node_from_edge(current_min_edge)
            self.remove_node(worst_node)#whichever you like (0 or 1)
            current_nodes.remove(worst_node)#care about the removed node
            super().add_node(new_node)
            self.add_weighted_edges_from([(new_node,n,new_node.distance(n)) for n in current_nodes])#care about the removed node
            return True

        #else
        return False


    def get_minimum_edge(self):
        return min(self.edges(data=True), key=lambda x: get_edge_distance(x))


    def get_worse_node_from_edge(self, edge):
        nodes = edge[0], edge[1]
        distances = [sum([get_edge_distance(e) for e in self.edges(node,data=True)]) for node in nodes]
        return nodes[argmin(distances)]


if __name__ == '__main__':
    from chromosome import chromosome
    chrs = [chromosome(3,3,(.2,.2,.3,.3),0,0) for _ in range(100)]

    nmap = novelty_map(10)
    import random
    for chr in chrs:
        chr.mutation(5)
        chr.make_spectrum()
        chr.fitness = random.random()
        print(nmap.add_node(chr))