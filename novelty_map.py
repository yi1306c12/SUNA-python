#!/usr/env/bin python3
import networkx as nx


class novelty_map(nx.Graph):

    def __init__(self,max_population):
        assert max_population > 0, "max_population must be > 0"
        self.max_population = max_population
        super().__init__()


    def append(self,new):
        new_distances = [new.distance(n) for n in self.nodes()]

        if len(self) < self.max_population:#if map is not full
            self.add_node(new)
            self.add_weighted_edges_from([(new,n,dist) for n,dist in zip(self.nodes(),new_distances)])#zip() iterates shortest times
            return True

        min_edge = self.min_weighted_edge()
        if min_edge[2]['weight'] < min(new_distances):#if map is full and new has more distance
            self.remove_node(min_edge[0])
            nodes_list = self.nodes()
            distance_list = [new.distance(n) for n in nodes_list]
            self.add_node(new)
            self.add_weighted_edges_from([(new,n,dist) for n,dist in zip(nodes_list,distance_list)])
            return True

        return False

    def min_weighted_edge(self):
        return min(self.edges(data=True),key=lambda x: x[2]['weight'])


if __name__ == '__main__':
    import random

    class test_gene(int):
        def distance(self,other):
            return (self-other)**2

    nm = novelty_map(100)
    l = list(range(1000))
    random.shuffle(l)
    for i in l:
        nm.append(test_gene(i))
    print(nm.nodes())
    s = sorted(nm.nodes())
    print(s)
    sub = [a-b for a,b in zip(s[1:],s[:-1])]
    print(sub)
    print([sub.count(i) for i in range(20)])
    print(list(range(20)))
    print(sum([sub.count(i) for i in range(20)]))


    #pos = nx.shell_layout(nm)
    #nx.draw_networkx(nm,pos)
    #nx.draw_networkx_edges(nm,pos)
    #edge_labels = dict(map(lambda x:((x[0],x[1]),str(x[2]['weight'])),nm.edges(data=True)))
    #nx.draw_networkx_edge_labels(nm,pos,edge_labels=edge_labels)
    #import matplotlib.pyplot as plt
    #plt.show()
