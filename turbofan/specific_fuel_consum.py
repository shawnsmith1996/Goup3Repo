#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from openmdao.api import ExplicitComponent,Problem, IndepVarComp
import numpy as np
from lsdo_utils.comps.arithmetic_comps.power_combination_comp import PowerCombinationComp
from lsdo_utils.comps.arithmetic_comps.linear_combination_comp import LinearCombinationComp

class Specific_Fuel_Consum(ExplicitComponent):

    def initialize(self):
        self.options.declare('e', types=float)
        
    def setup(self):
        self.add_input('B')
        self.add_input('k')
        self.add_input('M_inf')
        self.add_output('specific_fuel_consum')
        self.declare_partials('specific_fuel_consum', 'B')
        self.declare_partials('specific_fuel_consum', 'k')
        self.declare_partials('specific_fuel_consum', 'M_inf')

    def compute(self, inputs, outputs):
        B=inputs['B']
        k=inputs['k']
        M_inf=inputs['M_inf']
        
        outputs['specific_fuel_consum'] = B + B*k*M_inf
        
#        comp = LinearPowerCombinationComp(
#            shape=shape,
#            out_name='specific_fuel_consum',
#            term_list=[
#               (1,dict(
#                    M_inf=1.,
#                    k=1.,
#                    B=1.
#                )),
#            ],
#            constant=B,
#        )

    def compute_partials(self, inputs, partials):

        B=inputs['B']
        k=inputs['k']
        M_inf=inputs['M_inf']

        partials['specific_fuel_consum', 'B'] =1+k*M_inf
        
        partials['specific_fuel_consum', 'k'] =B*M_inf
        
        partials['specific_fuel_consum', 'M_inf'] =B*k




