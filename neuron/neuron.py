from abc import ABCMeta, abstractmethod


class neuron(metaclass=ABCMeta):

    def __init__(self, identical_number, adaptation_speed, initial_state = 0.):
        self.id = identical_number
        self.adaptation_speed = adaptation_speed
        self.internal_state = initial_state

    def __call__(self, x):
        self.internal_state += (self.activation(x) - self.internal_state)/self.adaptation_speed
        return self.internal_state

    @abstractmethod
    def activation(self, x):
        pass

if __name__ == '__main__':
    class neuron_test(neuron):
        def activation(self, x):
            return x

    nt = neuron_test(0, 1)

    import numpy as np
    print(nt(2))
    print(nt(np.array([1., 2.])))

    for _ in range(100):
        print(nt(2))
