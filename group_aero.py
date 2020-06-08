import numpy as np
from openmdao.api import Group, ExplicitComponent
from lsdo_utils.api import OptionsDictionary, LinearPowerCombinationComp,LinearCombinationComp, PowerCombinationComp, GeneralOperationComp, ElementwiseMinComp


class AeroGroup(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']



## Need CDv CD0 CL0 CLa 

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
