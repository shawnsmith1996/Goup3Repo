import numpy as np
from openmdao.api import Group, ExplicitComponent
from lsdo_utils.api import OptionsDictionary, LinearPowerCombinationComp,LinearCombinationComp, PowerCombinationComp, GeneralOperationComp, ElementwiseMinComp

class StructuresGroup(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']
        comp = PowerCombinationComp(
            shape=shape,
            out_name='aspect_ratio',
            powers_dict=dict(
                wing_span=1.,
                mean_chord=-1.,
            ),
        )
        self.add_subsystem('aspect_ratio', comp, promotes=['*'])