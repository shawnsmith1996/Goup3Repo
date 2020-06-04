import numpy as np
from openmdao.api import Group, ExplicitComponent

from structures.aspect_ratio import AspectRatio
from structures.gross_weight import GrossWeight

class StructuresGroup(Group):

    def setup(self):
        comp = AspectRatio()
        self.add_subsystem('aspect_ratio', comp, promotes=['*'])

        comp = GrossWeight()
        self.add_subsystem('gross_weight', comp, promotes=['*'])