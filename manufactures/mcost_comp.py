import numpy as np

from openmdao.api import ExplicitComponent


class MCcomp(ExplicitComponent):

#Ca : aircraft cost less engine
#Ce : cost per engine
#Ne : number of engines

    #def initialize(self):
        #self.options.declare('Ne', types=float)
        #self.options.declare('Ca', types=float)
        #self.options.declare('Ce', types=float

    def setup(self):
        self.add_input('Ca')
        self.add_input('Ce')
        self.add_input('Ne')
        self.add_output('maintcost')

        self.declare_partials('maintcost', 'Ca')
        self.declare_partials('maintcost', 'Ce')
        self.declare_partials('maintcost', 'Ne')

    def compute(self, inputs, outputs):
        Ca = inputs['Ca']
        Ce = inputs['Ce']
        Ne = inputs['Ne']

        outputs['maintcost'] = 3.3 * Ca / 10 ** 6 + 14.2 + 58 * Ce / 10 ** 6 * Ne - 26.1 * Ne
        
    def compute_partials(self, inputs, partials):

        Ca = inputs['Ca']
        Ce = inputs['Ce']
        Ne = inputs['Ne']
       
        partials['maintcost', 'Ca'] = 3.3 / 10 ** 6
        partials['maintcost', 'Ce'] = 8 / 10 ** 6 * Ne
        partials['maintcost', 'Ne'] = 58 * Ce / 10 ** 6 - 26.1
        
© 2020 GitHub, Inc.
