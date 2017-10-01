#!/usr/env/bin python3
from novelty_map_forSUNA import novelty_map
from chromosome import chromosome
from individual import individual

import random #choices

class SUNA:
    def __init__(self, number_of_inputs, number_of_outputs,
        initial_mutations = 200, step_mutations = 5, population_size = 100, maximum_novelty_map_population = 20, mutation_probability_array = (.01,.01,.49,.49),
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
        assert isinstance(population_size,int) and isinstance(maximum_novelty_map_population,int), "Population must be int"
        assert len(mutation_probability_array) == 4, "mutation_probability_array(M_pa) length must be 4"
        #assert all([0 <= probability <= 1 for probability in list(mutation_probability_array)+[neuromodulation_probability, control_neuron_probability]), "Probability must be 0 <= prob <= 1"

        self.novelty_map_size = maximum_novelty_map_population
        self.step_mutations = step_mutations
        self.excitation_threshold = excitation_threshold

        #first generation
        ancestor = chromosome(number_of_inputs, number_of_outputs, mutation_probability_array, neuromodulation_probability, control_neuron_probability)
        self.population = [ancestor.mutation(initial_mutations) for _ in range(population_size)]


    def generate_individuals(self):
        nov_map = novelty_map(self.novelty_map_size)

        for gene in self.population:
            ind = individual(gene,self.excitation_threshold)
            yield ind
            gene.fitness = ind.fitness
            nov_map.add_node(gene)

        self.mutation(list(nov_map.nodes()))

    def mutation(self,selected):
        #roullete choice
        children = [child.mutation(self.step_mutations) for child in random.choices(selected,k=len(self.population) - len(selected))]
        self.population = selected + children


if __name__ == '__main__':
    import gym
    env = gym.make('Pendulum-v0')
    inputs = env.observation_space.shape[0]

    suna = SUNA(inputs,1,maximum_novelty_map_population=10)

    iteration = 200
    steps = 100
    all_reward_list = []
    for g in range(iteration):
        print('generation :',g)
        reward_list = []
        for ind in suna.generate_individuals():
            accum_reward = 0
            observation, reward = env.reset(),0
            for s in range(steps):
                action = ind.process(observation)
                observation, reward, done, info = env.step(action)
                accum_reward += reward
                if done:
                    break
            ind.fitness = accum_reward
            reward_list.append(accum_reward)
        all_reward_list.append(reward_list)
        print(max(reward_list))




    #print result
