from neuron import neuron

print(dir(neuron))

class identity_neuron(neuron):
    def activation(self,x):
        return x

if __name__ == '__main__':
    identity_neuron(1,1)