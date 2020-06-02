#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from lsdo_utils.api import OptionsDictionary, LinearPowerCombinationComp,LinearCombinationComp, PowerCombinationComp, GeneralOperationComp, ElementwiseMinComp
from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver

from pressure_comp import PressureComp
from temperature_comp import TemperatureComp
from density_comp import DensityComp

from mach_num import Mach_Num


from zerospeed_thrust import Zerospeed_Thrust
from mass_flow import Mass_Flow_Rate
from specific_fuel_consum import Specific_Fuel_Consum
from thrust_ratio import Thrust_Ratio
from avaliable_thrust import Avaliable_Thrust
from thottled_thrust import Thottled_Thrust

class TurbofanGroup(Group):
   
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




# %%
