#!/usr/env/bin python3
from novelty_map import novelty_map
from chromosome import chromosome



class SUNA:
    def __init__(self, number_of_inputs, number_of_outputs,
        initial_mutations = 200, step_mutations = 5, populatio_size = 100, novelty_map_population = 20, mutation_probability_array = (.01,.01,.49,.49),
        neuromodulation_probability = .1, control_neuron_probability = .2, excitation_threshold = 0):
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

        #first generation
        self.population = [chromosome(number_of_inputs, number_of_outputs, mutation_probability_array).mutation(initial_mutations) for _ in range(population_size)]


    def generate_individuals(self):
        nov_map = novelty_map()

        for gene in self.population:
            ind = individual(gene)
            yield ind
            gene.fitness = ind.fitness
            nov_map.append(gene)

        self.mutation(nov_map.nodes())

    def mutation(self,selected):
        pass


if __name__ == '__main__':
    suna = SUNA(2,2)

    iteration = 5
    for g in range(iteration):
        for individual in generation:
            #evaluation

    #print result
