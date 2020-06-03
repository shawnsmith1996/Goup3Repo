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


from turbofan.zerospeed_thrust import Zerospeed_Thrust
from turbofan.mass_flow import Mass_Flow_Rate
from turbofan.specific_fuel_consum import Specific_Fuel_Consum
from turbofan.thrust_ratio import Thrust_Ratio
from turbofan.avaliable_thrust import Avaliable_Thrust
from turbofan.thottled_thrust import Thottled_Thrust
from turbofan.fuel_burn import Fuel_Burn

class TurbofanGroup(Group):
   ################################ NOTE INCOMING SEALEVEL THRUST MUST BE TWICE THE AMMOUNT NEEDED TO FLY TO ADJUST FOR THOTTLE ###################
    def setup(self):

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

        #### Thrust Compcomp = Zerospeed_Thrust()
        comp = Zerospeed_Thrust()
        self.add_subsystem('zerospeed_thrust_comp', comp, promotes=['*'])

        comp = Specific_Fuel_Consum()
        self.add_subsystem('specific_fuel_consum_comp', comp, promotes=['*'])

        comp = Thrust_Ratio()
        self.add_subsystem('thrust_ratio_comp', comp, promotes=['*'])

        comp = Avaliable_Thrust()
        self.add_subsystem('avaliable_thrust', comp, promotes=['*'])

        comp = Thottled_Thrust()
        self.add_subsystem('thottled_thrust_comp', comp, promotes=['*'])

        comp = Mass_Flow_Rate()
        self.add_subsystem('mass_flow_comp', comp, promotes=['*'])

        comp = Fuel_Burn()
        self.add_subsystem('fuel_burn_comp', comp, promotes=['*'])




# %%
