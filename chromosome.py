class chromosome:
    def __init__(self, n_inputs, n_outputs, M_pa):
        """M_pa = (add node, add connection, delete node, delete connection)"""
        self.M_pa = M_pa
        self.inputs = tuple([])
        self.outputs = tuple([])

        self.neurons = []
        self.connections = []

    def mutation(self,steps):
        pass
