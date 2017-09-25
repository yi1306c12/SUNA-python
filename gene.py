#This file should be divided in .py of each classes

class neuron_gene:

    def __init__(self, identical_number, adaptation_speed, neuron_type):
        self.id = identical_number
        self.adaptation_speed = adaptation_speed
        self.type = neuron_type

    def generate_phenotype(self, **keyargs):
        return self.type(self.id, self.adaptation_speed, **keyargs)


class connection_gene:

    def __init__(self, from_neuron_id, to_neuron_id, weight, modulation_id=-1):
        self.from_neuron_id = from_neuron_id
        self.to_neuron_id = to_neuron_id
        self.weight = weight
        self.modulation = modulation_id

    def weight_mutation(self):
        self.weight*=2#bug??
        


if __name__ == '__main__':
    class neuro_dummy:
        def __init__(self, identical_number, adaptation_speed):
            self.id = identical_number
            self.adaptation_speed = adaptation_speed

        def __call__(self, x):
            print(self.id,self.adaptation_speed)

    test = neuron_gene(1,1,neuro_dummy)
    neuron = test.generate_phenotype()
    neuron(10)
