#!/usr/bin/env python
# coding: utf-8

# In[12]:



from openmdao.api import ExplicitComponent
import numpy as np
from lsdo_utils.comps.arithmetic_comps.power_combination_comp import PowerCombinationComp
from lsdo_utils.comps.arithmetic_comps.linear_combination_comp import LinearCombinationComp

class Thrust_Ratio(ExplicitComponent):

    def initialize(self):
        self.options.declare('e', types=float)
        
    def setup(self):
        self.add_input('A')
        self.add_input('n')
        self.add_input('M_inf')
        self.add_output('thrust_ratio')
        self.declare_partials('thrust_ratio', 'A')
        self.declare_partials('thrust_ratio', 'n')
        self.declare_partials('thrust_ratio', 'M_inf')

    def compute(self, inputs, outputs):
        A=inputs['A']
        n=inputs['n']
        M_inf=inputs['M_inf']
        
        outputs['specific_fuel_consum'] = A*M_inf**(-n)
        
#        comp = LinearPowerCombinationComp(
#            shape=shape,
#            out_name='thrust_ratio',
#            term_list=[
#                (1,dict(
#                    M_inf=-n,
#                    A=1.,
#                )), 
#            ],
#        )

    def compute_partials(self, inputs, partials):

        A=inputs['A']
        n=inputs['n']
        M_inf=inputs['M_inf']

        partials['thrust_ratio', 'A'] =M_inf**(-n)
        
        partials['thrust_ratio', 'n'] =-np.log(M_inf)*A*M_inf**(-n)
        
        partials['thrust_ratio', 'M_inf'] =A*M_inf**(-n-1)




