#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

from openmdao.api import ExplicitComponent


class Mass_Flow_Rate(ExplicitComponent):

    def initialize(self):
        self.options.declare('e', types=float)

    def setup(self):
        self.add_input('thrust')
        self.add_input('mass_flow_rate_coeffecient')
        self.add_output('mass_flow_rate')

        self.declare_partials('CDi', 'CL')
        self.declare_partials('CDi', 'AR')
        
    def compute (self, inputs, outputs):
        thrust=inputs['thrust']
        mass_flow_rate_coeffecient=inputs['mass_flow_rate_coeffecient']

        
        outputs['mass_flow_rate'] = (thrust * mass_flow_rate_coeffecient)
        
#    def Mass_Flow_Rate(self, inputs, outputs):
 #       comp = PowerCombinationComp(
  #          shape=shape,
   #         out_name='mass_flow_rate',
    #        coeff=module['thrust_specific_fuel_consumption'],
     #       powers_dict=dict(
      #          thrust=1.,
       #     ),
        #)
    def compute_partials(self, inputs, partials):
        e = self.options['e']

        thrust=inputs['thrust']
        mass_flow_rate_coeffecient=inputs['mass_flow_rate_coeffecient']

        partials['mass_flow_rate', 'thrust'] = mass_flow_rate_coeffecient
        partials['mass_flow_rate', 'mass_flow_rate_coeffecient'] = thrust

