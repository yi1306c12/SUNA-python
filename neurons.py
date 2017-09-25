#This file should be divided in .py of each classes
from abc import ABCMeta, abstractmethod


class neuron(metaclass=ABCMeta):
    excitation = 0.
    def __init__(self, identical_number, adaptation_speed, initial_state = 0.):
        self.id = identical_number
        self.adaptation_speed = adaptation_speed
        self.internal_state = initial_state

    def __call__(self, x):
        self.internal_state += (self.activation(x) - self.internal_state)/self.adaptation_speed
        return self.internal_state

    def get_internal_state(self):
        return self.internal_state


    @abstractmethod
    def activation(self, x):
        pass


class identity_neuron(neuron):

    def activation(self,x):
        return x


import math


class sigmoid_neuron(neuron):
    def activation(self, x):
        return (math.tanh(x/2)+1)/2


class threshold_neuron(neuron):
    def activation(self,x):
        return 1. if x >= 0 else -1.


import random


class random_neuron(neuron):
    def activation(self,x):
        return random.uniform(-1,1)


class control_neuron(threshold_neuron):
    pass


class input_neuron:
    def set_internal_state(self,state):
        self.internal_state = state


class input_identity_neuron(input_neuron,identity_neuron):
    pass


class output_neuron:
    pass


class output_identity_neuron(output_neuron, identity_neuron):
    pass

    
if __name__ == "__main__":
    #test input_neuron
    iin = input_identity_neuron(0, 1)
    iin.set_internal_state(1)
    print(iin.get_internal_state())