import numpy as np

from openmdao.api import ExplicitComponent


class Empty_Weight(ExplicitComponent):

    #def initialize(self):
        #self.options.declare('Q', types=float)
        #self.options.declare('FTA', types=float)

    def setup(self):
        self.add_input('crew_weight')
        self.add_input('payload_weight')
        self.add_input('gross_weight')
        self.add_input('Wfr') #Fuel Weight?
        self.add_output('We')

        self.declare_partials('We', 'gross_weight')

    def compute(self, inputs, outputs):
        crew_weight = inputs['crew_weight']
        payload_weight = inputs['payload_weight']
        gross_weight = inputs['gross_weight']
        Wfr = inputs['Wfr'] #fuel weight?

        outputs['We'] = gross_weight-(crew_weight + payload_weight + Wfr*gross_weight)

    def compute_partials(self, inputs, partials):
        Wfr = inputs['Wfr']
        partials['We', 'gross_weight'] = 1 - Wfr

