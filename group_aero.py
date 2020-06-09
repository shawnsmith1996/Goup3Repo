import numpy as np
from openmdao.api import Group, ExplicitComponent
from lsdo_utils.api import OptionsDictionary, LinearPowerCombinationComp,LinearCombinationComp, PowerCombinationComp, GeneralOperationComp, ElementwiseMinComp
from turbofan.atmosphere.pressure_comp import PressureComp
from turbofan.atmosphere.temperature_comp import TemperatureComp
from turbofan.atmosphere.density_comp import DensityComp

class AeroGroup(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)
        self.options.declare('name', types=str)
        
    def setup(self):
        shape = self.options['shape']



## Need CDv CD0 CL0 CLa 
#comp = PressureComp()
 #self.add_subsystem('pressure_comp', comp, promotes=['*'])

#comp = TemperatureComp()
#self.add_subsystem('temperature_comp', comp, promotes=['*'])

#comp = DensityComp() 
#self.add_subsystem('density_comp', comp, promotes=['*'])


        comp = PowerCombinationComp(
            shape=shape,
            coeff=1/2,
            out_name='drag',
            powers_dict=dict(
                speed=2.,
                density=1,
                drag_coeff = 1.,
            )
        )
        self.add_subsystem('drag_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='Lift',
            powers_dict=dict(
                drag = 1.,
                lift_to_drag_ratio = 1
            )
        )
        self.add_subsystem('lift_comp', comp, promotes=['*'])
