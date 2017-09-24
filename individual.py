import numpy as np

class individual:
    def __init__(self, chromosome):
        self.input_neurons = [n.generate_phenotyoe() for n in chromosome.inputs]
        self.output_neurons = [n.generate_phenotyoe() for n in chromosome.outputs]
        self.neurons = [n.generate_phenotype() for n in chromosome.neurons]
        self.controls = [cn.generate_phenotype() for cn in chromosome.control_neurons]

        self.connections = chromosome.connections

        #make primer list
        control_ids = [cn.id for cn in self.controls]
        nonprimer_ids = set([conn.to_neuron for conn in self.control_connections if conn.to_neuron in control_ids])
        primer_ids = set(control_ids) - nonprimer_ids
        self.primer_neurons = [cn for cn in self.controls if cn.id in primer_ids]

    def process(self, observation):
        modulation =
