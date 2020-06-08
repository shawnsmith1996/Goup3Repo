#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from lsdo_utils.api import OptionsDictionary, LinearPowerCombinationComp,LinearCombinationComp, PowerCombinationComp, GeneralOperationComp, ElementwiseMinComp
from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver

from turbofan.specific_fuel_consum import Specific_Fuel_Consum
from turbofan.thrust_ratio import Thrust_Ratio
from turbofan.thottled_thrust import Thottled_Thrust
from turbofan.fuel_burn import Fuel_Burn

class TurbofanGroup(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)
   ################################ NOTE INCOMING SEALEVEL THRUST MUST BE TWICE THE AMMOUNT NEEDED TO FLY TO ADJUST FOR THOTTLE ###################
    def setup(self):
        shape = self.options['shape']
        #computations below: 


        #### Thrust Compcomp = Zerospeed_Thrust()
        sealv_dens=1.225
        comp = PowerCombinationComp(
            shape=shape,
            coeff=1/sealv_dens,
            out_name='zerospeed_thrust',
            powers_dict=dict(
                T_max=1.,
                density=1.,
            )
        )
        self.add_subsystem('zerospeed_thrust_comp', comp, promotes=['*'])

        comp=Specific_Fuel_Consum()
        self.add_subsystem('specific_fuel_consum_comp', comp, promotes=['*'])

        comp=Thrust_Ratio()
        self.add_subsystem('thrust_ratio_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='avaliable_thrust',
            powers_dict=dict(
                thrust_ratio=1.,
                zerospeed_thrust=1.,
            ),
        )
        self.add_subsystem('avaliable_thrust', comp, promotes=['*'])

        comp=Thottled_Thrust()
        self.add_subsystem('thottled_thrust_comp', comp, promotes=['*'])

        mass_flow_rate_coeffecient=0.61   
        comp = PowerCombinationComp(
            shape=shape,
            out_name='mass_flow_rate',
            coeff=mass_flow_rate_coeffecient,
            powers_dict=dict(
                thottled_thrust=1.,
            ),
        )
        self.add_subsystem('mass_flow_comp', comp, promotes=['*'])





# %%
