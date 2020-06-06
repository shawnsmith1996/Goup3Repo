import numpy as np
from openmdao.api import Group, ExplicitComponent


class StructuresGroup(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        comp = PowerCombinationComp(
            shape=shape,
            out_name='aspect_ratio',
            powers_dict=dict(
                wing_span=1.,
                chord=-1.,
            ),
        )
        self.add_subsystem('aspect_ratio', comp, promotes=['*'])