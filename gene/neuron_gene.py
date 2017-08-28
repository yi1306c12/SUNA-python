class neuron_gene:

    def __init__(self, identical_number, adaptation_speed, neuron_type):
        self.id = identical_number
        self.adaptation_speed = adaptation_speed
        self.type = neuron_type

    def generate_phenotype(self, **keyargs):
        return self.type(self.id, self.adaptation_speed, **keyargs)


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
