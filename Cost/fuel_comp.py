import numpy as np

from openmdao.api import ExplicitComponent


class FuelComp(ExplicitComponent):


    def setup(self):
        self.add_input('We')
        self.add_input('Wfr')
        #self.add_input('M_max')
        self.add_output('Fuel')

        self.declare_partials('Fuel', 'We')
        self.declare_partials('Fuel', 'Wfr')

    def compute(self, inputs, outputs):
        
        We = inputs['We']
        Wfr = inputs['Wfr']

        outputs['Fuel'] = Wfr*We*6.7*0.896

    def compute_partials(self, inputs, partials):

        We = inputs['We']
        #SFC = inputs['specific_fuel_consum']
        Wfr = inputs['Wfr']
        
        partials['Fuel', 'We'] = Wfr*6.7*0.896
        partials['Fuel', 'Wfr'] = We*6.7*0.896
