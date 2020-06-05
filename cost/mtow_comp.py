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
        self.add_input('Wfr') #Fuel Weight?
        self.add_output('MTOW')

        self.declare_partials('MTOW', 'We')
        self.declare_partials('MTOW', 'Wfr')

    def compute(self, inputs, outputs):
        crew_weight = inputs['crew_weight']
        payload_weight = inputs['payload_weight']
        We = inputs['We']
        Wfr = inputs['Wfr'] #fuel weight?

        outputs['MTOW'] = crew_weight+payload_weight+We+Wfr

    def compute_partials(self, inputs, partials):

        partials['MTOW', 'We'] = 1
        partials['MTOW', 'Wfr'] =1
