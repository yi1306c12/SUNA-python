from neuron import neuron

class threshold_neuron(neuron):
    def activation(self,x):
        return 1. if x >= 0 else -1.
