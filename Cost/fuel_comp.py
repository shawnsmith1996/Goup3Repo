import numpy as np

from openmdao.api import ExplicitComponent


class FuelComp(ExplicitComponent):


    def setup(self):
        self.add_input('W0')
        self.add_input('Wfr')
        #self.add_input('M_max')
        self.add_output('Fuel')

        self.declare_partials('Fuel', 'W0')
        self.declare_partials('Fuel', 'Wfr')

    def compute(self, inputs, outputs):
        
        We = inputs['W0']
        Wfr = inputs['Wfr']

        outputs['Fuel'] = Wfr*W0*6.7*0.896

    def compute_partials(self, inputs, partials):

        We = inputs['W0']
        #SFC = inputs['specific_fuel_consum']
        Wfr = inputs['Wfr']
        
        partials['Fuel', 'W0'] = Wfr*6.7*0.896
        partials['Fuel', 'Wfr'] = W0*6.7*0.896
