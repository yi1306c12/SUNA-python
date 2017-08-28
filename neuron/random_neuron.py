from neuron import neuron
import random

class random_neuron(neuron):
    def activation(self,x):
        return random.uniform(-1,1)
