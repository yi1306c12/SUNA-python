#!/usr/env/bin python3
from novelty_map import novelty_map

class SUNA:
    def __init__(self, initial_mutations, step_mutations, population_size, maximum_novelty_map_population, mutation_probability_array, neuromodulation_probability, control_neuron_probability, excitation_threshold):
        """
        initial_mutations                   :
        step_mutations                      :
        population_size                     :
        maximum_novelty_map_population      :
        mutation_probability_array          :[add node, add connection, delete node, delete connection]
        neuromodulation_probability         :Probability makes a new node control_neuron in add_node mutation
        control_neuron_probability          :Probability makes a new connection from control neuron in add_connection mutation
        excitation_threshold                :for control signal
        """
        assert isinstance(initial_mutations,int) and isinstance(step_mutations,int), "Number of mutations must be int"
        assert isinstance(population_size,int) and isinstance(maximum_novelty_map_population), "Population must be int"
        assert len(mutation_probability_array) == 4, "mutation_probability_array(M_pa) length must be 4"
        assert all([0 <= probability <= 1 for probability in list(mutation_probability_array)+[neuromodulation_probability, control_neuron_probability]), "Probability must be 0 <= prob <= 1"

        #initial mutations
        self.genes


    def generate_individuals(self):
        nov_map = novelty_map()

        for gene in self.genes:
            ind = individual(gene)
            yield ind
            gene.fitness = ind.fitness
            nov_map.append(gene)

        self.mutation(nov_map.nodes())

    def mutation(self,genes):
        pass

if __name__ == '__main__':
    I_m = 200
    S_m = 5
    lenP = 100
    Max_n = 20
    M_pa = (.01, .01, .49, .49)
    Neuromodulation_P = .1
    Control_neuron_P = .2
    Excitation_threshold = .0

    suna = SUNA(I_m, S_m, lenP, Max_n, M_pa, Neuromodulation_P, Control_neuron_P, Excitation_threshold)

    iteration = 5
    for g in range(iteration):
        for individual in generation:
            #evaluation

    #print result
