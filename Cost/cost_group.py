import numpy as np
from openmdao.api import Group, ExplicitComponent

from fl_comp import FlyawayComp
from fuel_comp import FuelComp
from main_comp import MainComp
from rdte_comp import RDTEComp

class CostGroup(Group):
    
    def setup(self):
        comp = FlyawayComp()
        self.add_subsystem('fl_comp', comp, promotes=['*'])

        comp = FuelComp()
        self.add_subsystem('fuel_comp', comp, promotes=['*'])

        comp = MainComp()
        self.add_subsystem('main_comp', comp, promotes=['*'])

        comp = RDTEComp()
        self.add_subsystem('rdte_comp', comp, promotes=['*'])