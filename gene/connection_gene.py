class connection_gene:
    def __init__(self, from_neuron_id, to_neuron_id, weight, modulation_id=-1):
        self.from_neuron = from_neuron_id
        self.to_neuron = to_neuron_id
        self.weight = weight
        self.modulation = modulation_id
