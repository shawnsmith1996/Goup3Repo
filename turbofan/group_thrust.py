#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from lsdo_utils.api import OptionsDictionary, LinearPowerCombinationComp,LinearCombinationComp, PowerCombinationComp, GeneralOperationComp, ElementwiseMinComp
from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver



from .pressure_comp import PressureComp
from .temperature_comp import TemperatureComp
from .density_comp import DensityComp


from .specific_fuel_consum import Specific_Fuel_Consum
from .thrust_ratio import Thrust_Ratio
from .thottled_thrust import Thottled_Thrust
from .fuel_burn import Fuel_Burn

class TurbofanGroup(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)
   ################################ NOTE INCOMING SEALEVEL THRUST MUST BE TWICE THE AMMOUNT NEEDED TO FLY TO ADJUST FOR THOTTLE ###################
    def setup(self):
        shape = self.options['shape']
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
        R=287.058
        gamma=1.4
        comp = PowerCombinationComp(#
            shape=shape,
            coeff=1/np.sqrt(gamma*R),
            out_name='M_inf',
            powers_dict=dict(
                velocity_ms=1.,
                temperature=-0.5,
            )
        )
        self.add_subsystem('mach_comp', comp, promotes=['*'])
        ## Mach num calc above

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
                thrust=1.,
            ),
        )
        self.add_subsystem('mass_flow_comp', comp, promotes=['*'])





# %%
