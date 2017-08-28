from neuron import neuron,identity_neuron,sigmoid_neuron,random_neuron,threshold_neuron,
                    input_identity_neuron,output_identity_neuron,control_neuron
from gene import neuron_gene, connection_gene
normal_neurons = [identity_neuron,sigmoid_neuron,random_neuron,threshold_neuron]

import random

class chromosome:
    def __init__(self, n_inputs, n_outputs, M_pa):
        """M_pa = (add node, add connection, delete node, delete connection)"""
        self.M_pa = M_pa
        self.inputs = tuple([neuron_gene(i,1,input_identity_neuron) for i in range(n_inputs)])
        self.outputs = tuple([neuron_gene(i+n_inputs,1,output_identity_neuron) for i in range(n_outputs)])

        self.neurons = []
        self.control_neurons = []

        self.connections = []
        self.control_connections = []

    def mutation(self,steps):
        pass

    def add_neuron(self):
        pass

    def delete_neuron(self):
        pass

    def add_connection(self):
        pass

    def delete_connection(self):
        connection = random.choice(self.connections+self.control_neurons)
