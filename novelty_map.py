#!/usr/env/bin python3
import networkx as nx


class novelty_map(nx.Graph):

    def __init__(self,max_population):
        self.max_population = max_population
        super().__init__()


    def append(self,new):
        new_distances = [new.distance(n) for n in self.nodes()]
        min_edge = self.min_weighted_edge()

        if len(self) < self.max_population:#if map is not full
            self.add_node(new)
            self.add_weighted_edges_from([(new,n,dist) for n,dist in zip(self.nodes(),new_distances)])#zip() iterates shortest times
            return True

        elif min_edge[2]['weight'] < min(new_distances):#if map is full and new has more distance
            self.remove_node(min_edge[0])
            distance_list = [new.distance(n) for n in self.nodes()]
            nodes_list = self.nodes()
            self.add_node(new)
            self.add_weighted_edges_from([(new,n,dist) for n,dist in zip(nodes_list,distance_list)])
            return True

        return False

    def min_weighted_edge(self):
        return min(self.edges(data=True),key=lambda x: x[2]['weight'])


if __name__ == '__main__':
    class test_gene(int):
        def distance(self,other):
            return (self**2-other**2)**1
    nm = novelty_map(100)
    for i in range(150):
        nm.append(test_gene(i))

    #pos = nx.shell_layout(nm)
    #nx.draw_networkx(nm,pos)
    #nx.draw_networkx_edges(nm,pos)
    #edge_labels = dict(map(lambda x:((x[0],x[1]),str(x[2]['weight'])),nm.edges(data=True)))
    #nx.draw_networkx_edge_labels(nm,pos,edge_labels=edge_labels)
    #import matplotlib.pyplot as plt
    #plt.show()
