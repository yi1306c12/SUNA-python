from phenotype import control_neuron, modulated_connection, connection_phenotype


class individual:
    #parameter
    REMAINING_NEURON_THRESHOLD = 1e-3

    def __init__(self, chromosome, EXCITATION_THRESHOLD):
        #parameters
        self.EXCITATION_THRESHOLD = EXCITATION_THRESHOLD

        #neurons
        self.input_neurons = [n.generate_phenotype() for n in chromosome.inputs]
        self.output_neurons = [n.generate_phenotype() for n in chromosome.outputs]
        self.neurons = [n.generate_phenotype() for n in chromosome.neurons]
        self.controls = [cn.generate_phenotype() for cn in chromosome.control_neurons]

        all_neurons = self.input_neurons + self.output_neurons + self.neurons + self.controls
        neuron_dict = {n.id:n for n in all_neurons}#id dict

        #make connections
        self.connections = []
        for genotype_conn in chromosome.connections:
            from_neuron = neuron_dict[genotype_conn.from_neuron_id]
            to_neuron = neuron_dict[genotype_conn.to_neuron_id]
            if genotype_conn.modulation < 0:
                phenotype_conn = connection_phenotype(from_neuron, to_neuron, genotype_conn.weight)
            else:
                phenotype_conn = modulated_connection(from_neuron, to_neuron, neuron_dict[genotype_conn.modulation], self.EXCITATION_THRESHOLD)
            self.connections.append(phenotype_conn)

        #execute preparation
        self.source_dict = {to_neuron
            : [conn for conn in self.connections if conn.to_neuron is to_neuron and not isinstance(conn.from_neuron,control_neuron)]#no controls
            for to_neuron in all_neurons}
        self.from_control_dict = {from_control_neuron
            : [conn for conn in self.connections if conn.from_neuron is from_control_neuron]#from control_neuron connections
            for from_control_neuron in self.controls}

        #make primer list
        from_control_connections = [conn for conn in self.connections if conn.from_neuron in self.controls]
        self.nonprimer_neurons = list(set([conn.to_neuron for conn in from_control_connections if conn.to_neuron in self.controls]))
        self.primer_neurons = list(set(self.controls) - set(self.nonprimer_neurons))
#        print(len(self.nonprimer_neurons),len(self.primer_neurons))


    def execute(self, to_neuron, addition=0.):
        return sum([conn() for conn in self.source_dict[to_neuron]]) + addition


    def control_execute(self, from_control_neuron):
        for connection in self.from_control_dict[from_control_neuron]:
            connection.to_neuron.excitation += connection()


    def process(self, observation):
        assert len(self.input_neurons) == len(observation), "invalid input length {}->{}".format(len(observation),len(self.input_neurons))

#input neurons
        for input_neuron, s in zip(self.input_neurons, observation):
            self.execute(input_neuron, addition=s)
#            print('inputs :',self.execute(input_neuron,addition=s),input_neuron.get_internal_state())

#primer neurons
        for primer_neuron in self.primer_neurons:
            self.execute(primer_neuron)
        for primer_neuron in self.primer_neurons:
            self.control_execute(primer_neuron)

#the other control neurons
        yet_fired = self.nonprimer_neurons.copy()
        while True:
            activated_neurons = [activated for activated in yet_fired if activated.excitation > self.EXCITATION_THRESHOLD]
            #if no change,break this loop.
            if not activated_neurons : break

            for activated_neuron in activated_neurons:
                self.execute(activated_neuron)
                yet_fired.remove(activated_neuron)

            for activated_neuron in activated_neurons:
                self.control_execute(activated_neuron)
            
#normal neurons
        remaining_neurons = [n for n in self.neurons if n.excitation >= self.EXCITATION_THRESHOLD] + self.output_neurons
        while True:
            activated_neurons = []
            for tested_neuron in remaining_neurons:
                if -self.REMAINING_NEURON_THRESHOLD < self.execute(tested_neuron) < self.REMAINING_NEURON_THRESHOLD:
                    pass
                else:
                    activated_neurons.append(tested_neuron)
                    remaining_neurons.remove(tested_neuron)
            #if no effective change, break this loop.
            if not activated_neurons : break
        #output neurons should be activated anyway
        for remained_neuron in remaining_neurons:
            if remained_neuron in self.output_neurons:
                self.execute(remained_neuron)
#        print('remained :', remaining_neurons)

#neurons reset
#        print('excitation :',sum([n.excitation for n in self.input_neurons+self.output_neurons+self.neurons+self.controls]))
        for n in self.input_neurons + self.output_neurons + self.neurons + self.controls:
            n.excitation = 0.

#output result
        return [on.internal_state for on in self.output_neurons]


if __name__ == '__main__':
    from chromosome import chromosome
    chr = chromosome(3,2,(0.01,0.01,0.49,0.49),0,0)
    for _ in range(10):
        chr.add_connection()
    chr.generate_graph()
    print(chr.connections)
    ind = individual(chr,0.)
    print(ind.process([0,1,2]))
    print(ind.process([0,1,2]))
    print(ind.process([0,1,2]))