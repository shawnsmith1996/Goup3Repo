import numpy as np
from openmdao.api import Group, ExplicitComponent

from structures.aspect_ratio import AspectRatio


class StructuresGroup(Group):

    def setup(self):
        comp = AspectRatio()
        self.add_subsystem('aspect_ratio', comp, promotes=['*'])