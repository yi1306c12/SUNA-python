import random
from functools import reduce
from neuron import neuron,identity_neuron,sigmoid_neuron,random_neuron,threshold_neuron,
                    input_identity_neuron,output_identity_neuron,control_neuron
from gene import neuron_gene, connection_gene


normal_neurons = [identity_neuron,sigmoid_neuron,random_neuron,threshold_neuron]
firing_rate_levels = [1,7,49]


class chromosome:
    def __init__(self, n_inputs, n_outputs, M_pa, neuromodulation_probability, control_neuron_probability, excitation_threshold):
        """M_pa = (add node, add connection, delete node, delete connection)"""
        self.M_pa = M_pa
        self.neuromodulation_probability, self.control_neuron_probability = neuromodulation_probability, control_neuron_probability
        self.excitation_threshold = excitation_threshold

        #fixed interface neurons
        self.inputs = tuple([neuron_gene(i,1,input_identity_neuron) for i in range(n_inputs)])
        self.outputs = tuple([neuron_gene(i+n_inputs,1,output_identity_neuron) for i in range(n_outputs)])

        self.neurons = []
        self.control_neurons = []

        self.connections = []
        self.control_connections = []

    def mutation(self,steps mutation_probability = None):
        #in > python 3.6
        #random.choices(operations,weights=mutation_probability)
        import numpy
        operations = [self.add_neuron, self.delete_neuron, self.add_connection, self.delete_connection]
        if mutation_probability is None:
            mutation_probability = self.M_pa
        for _ in range(steps)
            numpy.random.choice(operations, p=mutation_probability)()#operation at random

    def find_smallest_id(self, neurons_list):
        #find smallest id not used
        neuron_ids = [n.id for n in neurons_list]
        remain_ids = list(range(len(all_neurons))).difference(all_neurons_id)
        if len(remain_ids) > 0:
            remain_ids.sort()
            return remain_ids[0]
        else:
            return max(neuron_ids) + 1


    def add_neuron(self):
        all_neurons = self.inputs + self.outputs + self.neurons + self.control_neurons
        #make new neuron
        new = neuron_gene(
                self.find_smallest_id(all_neurons),
                random.choice(firing_rate_levels),
                control_neuron if random.random()<self.control_neuron_probability else random.choice(normal_neurons)
                )
        #make new connections
        self.add_connection_from_lists(all_neurons, [new], all_neurons)
        self.add_connection_from_lists([new], all_neurons, all_neurons)


    def delete_neuron(self):
        if len(self.neurons + self.control_neurons) == 0:
            return#guard

        delete = random.choice(self.neurons + self.control_neurons)
        for n_list in (self.neurons, self.control_neurons):
            if delete in n_list:
                n_list.remove(delete)
                break
        #delete all connections relate the deleted neuron
        connections_lists = [self.connections, self.control_connections]
        for c_list in connections_lists:
            for c in c_list:
                if c.from_neuron == delete.id or c.to_neuron == delete.id or c.modulation == delete.id:
                    c_list.remove(c)
        
    def add_connection(self):
        all_neurons = self.inputs + self.outputs + self.neurons + self.control_neuron
        add_connection_from_lists(self, all_neurons, all_neurons, all_neurons)

    def add_connection_from_lists(self, from_list, to_list, modulator_list):
        from_neuron, to_neuron = random.choice(from_list), random.choice(to_list)
        
        if random.random() < self.neuromodulation_probability:
            modulator = random.choice(modulator_list)
            new_connection = connection_gene(from_neuron.id, to_neuron.id, 1, modulator.id)
        else:
            weight = random.choice([-1,1])
            new_connection = connection_gene(from_neuron.id, to_neuron.id, weight)

        if isinstance(from_neuron,control_neuron):
            self.control_connections.append(new_connection)
        else:
            self.connections.append(new_connection)


    def delete_connection(self):
        connections_lists = [self.connections, self.control_connections]
        if len(connections_lists) == 0:
            return#guard

        connection = random.choice(reduce(lambda x,y:x+y, connections_lists))
        for c_list in connections_lists:
            if connection in c_list:
                c_list.remove(connection)
                break
