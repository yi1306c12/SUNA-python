from neuron import neuron
import math

class sigmoid_neuron(neuron):
    def activation(self, x):
        return (math.tanh(x/2)+1)/2
