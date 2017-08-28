from neuron import neuron

class identity_neuron(neuron):
    def activation(self,x):
        return x
