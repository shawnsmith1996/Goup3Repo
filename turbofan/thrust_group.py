#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from openmdao.api import Group, IndepVarComp
from lsdo_utils.api import OptionsDictionary, LinearCombinationComp, PowerCombinationComp, GeneralOperationComp, ElementwiseMinComp
class TurbofanGroup(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)
        self.options.declare('part', types=OptionsDictionary)
        self.promotes = ['sealv_thrust']
        
    def setup(self):
        shape = self.options['shape']
        module = self.options['options_dictionary']
        part = self.options['part']
        
        comp = IndepVarComp()
        comp.add_input('sealevel_thrust')
        comp.add_input('density')
        comp.add_input('sealevel_density')
        comp.add_output('avaliable_thrust')

        comp.add_input('throttle')
        comp.add_output('thrust')

        comp.add_input('mass_flow_rate_coeffecient')
        comp.add_output('mass_flow_rate')


        comp.add_input('B')
        comp.add_input('k')
        comp.add_input('M_inf')
        comp.add_output('specific_fuel_consum')

        comp.add_input('A')
        comp.add_input('n')    
        comp.add_output('thrust_ratio')
        self.add_subsystem('inputs_comp', comp, promotes=['*'])
        
        comp = PowerCombinationComp(
            shape=shape,
            out_name='available_thrust',
            powers_dict=dict(
                mach_number=0.,
                sealevel_thrust=1.,
                density=1.,
                sealevel_density=-1.,
            )
        )
        prob.model.add_subsystem('available_thrust_comp',comp,promote=['*'])


        comp = PowerCombinationComp(
            shape=shape,
            out_name='mass_flow_rate',
            coeff=module['thrust_specific_fuel_consumption'],
            powers_dict=dict(
                thrust=1.,
            ),
        )
        prob.model.add_subsystem('mass_flow_rate_comp',comp,promote=['*'])
        
        comp = PowerCombinationComp(
            shape=shape,
            out_name='thrust',
            powers_dict=dict(
                throttle=1.,
                available_thrust=1.,
            ),
        )
        prob.model.add_subsystem('thrust_comp',comp,promote=['*'])
        
        comp = LinearPowerCombinationComp(
            shape=shape,
            out_name='specific_fuel_consum',
            term_list=[
                (1,dict(
                    M_inf=1.,
                    k=1.,
                    B=1.
                )),
            ],
            constant=B,
        )
        prob.model.add_subsystem('specific_fuel_consum_comp',comp,promote=['*'])
        
        n=part['n']
        comp = LinearPowerCombinationComp(
            shape=shape,
            out_name='thrust_ratio',
            term_list=[
                (1,dict(
                    M_inf=-n,
                    A=1.,
                )), 
            ],
        )
        prob.model.add_subsystem('thrust_ratio_comp',comp,promote=['*'])



# %%
