from neurons import control_neuron

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

        self.connections = chromosome.connections

        #make primer list
        control_ids = [cn.id for cn in self.controls]
        from_control_connections = [conn for conn in self.connections if conn.from_neuron_id in control_ids]
        nonprimer_ids = set([conn.to_neuron_id for conn in from_control_connections if conn.to_neuron_id in control_ids])
        primer_ids = set(control_ids) - nonprimer_ids
        self.nonprimer_neurons = [cn for cn in self.controls if cn.id in nonprimer_ids]
        self.primer_neurons = [cn for cn in self.controls if cn.id in primer_ids]

        self.all_neurons = self.input_neurons + self.output_neurons + self.neurons + self.controls
        self.neuron_dict = {n.id:n for n in self.all_neurons}#id dict


    def execute(self, neuron, addition=0.):
        all_input_sum = 0.

        for connection in self.connections:
            #is input to this neuron?
            if connection.to_neuron_id != neuron.id : continue#guard

            #is not control_neuron?
            source_neuron = self.neuron_dict[connection.from_neuron_id]
            if isinstance(source_neuron, control_neuron) : continue#guard

            #no modulation
            if connection.modulation < 0:
#                print('input from', source_neuron.id, source_neuron.get_internal_state())
                _input = connection.weight * source_neuron.get_internal_state()
            #neuromodulation
            else:
                modulator_neuron = self.neuron_dict[connection.modulation]
                modulator_input = modulator_neuron.get_internal_state() if modulator_neuron.excitation >= self.EXCITATION_THRESHOLD else 0.
                _input = modulator_input * source_neuron.get_internal_state()

            all_input_sum += _input

        #update internal state
#        print(neuron.id,all_input_sum)
        return neuron(all_input_sum + addition)


    def control_execute(self, neuron):
        for connection in self.connections:
            #is excited by this control neuron?
            if connection.from_neuron_id != neuron.id : continue#guard
            
            destination_neuron = self.neuron_dict[connection.to_neuron_id]
            #no modulation
            if connection.modulation < 0:
                destination_neuron.excitation += connection.weight*neuron.get_internal_state()
            #neuromodulation
            else:
                modulator_neuron = self.neuron_dict[connection.modulation]
                modulator_input = modulator_neuron.get_internal_state() if modulator_neuron.excitation >= self.EXCITATION_THRESHOLD else 0.
                destination_neuron.excitation += modulator_input * neuron.get_internal_state()
        

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
        print('remained :', remaining_neurons)

#neurons reset
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