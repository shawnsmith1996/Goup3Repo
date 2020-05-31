#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from lsdo_utils.api import OptionsDictionary, LinearPowerCombinationComp,LinearCombinationComp, PowerCombinationComp, GeneralOperationComp, ElementwiseMinComp
from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver

from turbofan.pressure_comp import PressureComp
from turbofan.temperature_comp import TemperatureComp
from turbofan.density_comp import DensityComp

from turbofan.mach_num import Mach_Num

from turbofan.avaliable_thrust import Avaliable_Thrust
from turbofan.thrust import Thrust
from turbofan.mass_flow import Mass_Flow_Rate
from turbofan.specific_fuel_consum import Specific_Fuel_Consum
from turbofan.thrust_ratio import Thrust_Ratio

class TurbofanGroup(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)
        self.options.declare('options_dictionary')
        
    def setup(self):
        shape = self.options['shape']
        module = self.options['options_dictionary']

        #computations below: 
        #### Atmosphere Comp
        comp = PressureComp()
        self.add_subsystem('pressure_comp', comp, promotes=['*'])

        comp = TemperatureComp()
        self.add_subsystem('temperature_comp', comp, promotes=['*'])

        comp = DensityComp() 
        self.add_subsystem('density_comp', comp, promotes=['*'])
        ## Atmosphere above

        # Mach Num Comp
        comp= Mach_Num()
        self.add_subsystem('mach_comp', comp, promotes=['*'])
        ## Mach num calc above

        #### Thrust Comp
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
        self.add_subsystem('available_thrust_comp',comp,promotes=['*'])


        comp = PowerCombinationComp(
            shape=shape,
            out_name='mass_flow_rate',
            coeff=module['thrust_specific_fuel_consumption'],
            powers_dict=dict(
                thrust=1.,
            ),
        )
        self.add_subsystem('mass_flow_rate_comp',comp,promotes=['*'])
        
        comp = PowerCombinationComp(
            shape=shape,
            out_name='thrust',
            powers_dict=dict(
                throttle=1.,
                available_thrust=1.,
            ),
        )
        self.add_subsystem('thrust_comp',comp,promotes=['*'])
        
        comp = LinearPowerCombinationComp(
            shape=shape,
            out_name='specific_fuel_consum',
            term_list=[
                (1,dict(
                    M_inf=1.,
                    k=1.,
                    B=1.
                )),
                (1,dict(
                    B=1
                ))
            ],
        )
        self.add_subsystem('specific_fuel_consum_comp',comp,promotes=['*'])
        
        comp=Specific_Fuel_Consum()
        self.add_subsystem('thrust_ratio_comp',comp,promotes=['*'])



# %%
