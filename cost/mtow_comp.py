import numpy as np

from openmdao.api import ExplicitComponent


class MTOWComp(ExplicitComponent):

    #def initialize(self):
        #self.options.declare('Q', types=float)
        #self.options.declare('FTA', types=float)

    def setup(self):
        self.add_input('crew_weight')
        self.add_input('payload_weight')
        self.add_input('We')
        self.add_input('gross_weight')
        self.add_input('Wfr') #Fuel Weight?
        self.add_output('MTOW')

        self.declare_partials('MTOW', 'We')
        self.declare_partials('MTOW', 'gross_weight')

    def compute(self, inputs, outputs):
        crew_weight = inputs['crew_weight']
        payload_weight = inputs['payload_weight']
        We = inputs['We']
        fuel_weight_fraction = inputs['Wfr'] #fuel weight?
        gross_weight=inputs['gross_weight']

        outputs['MTOW'] = crew_weight + payload_weight + We + fuel_weight_fraction*gross_weight

    def compute_partials(self, inputs, partials):
        fuel_weight_fraction = inputs['Wfr']
        partials['MTOW', 'We'] = 1
        partials['MTOW', 'gross_weight'] =fuel_weight_fraction
