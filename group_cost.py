import numpy as np
from openmdao.api import Group, ExplicitComponent

from cost.fl_comp import FlyawayComp
from cost.fuel_comp import FuelComp
from cost.main_comp import MainComp
from cost.rdte_comp import RDTEComp
from cost.mtow_comp import MTOWComp

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
        
        comp = MTOWComp()
        self.add_subsystem('mtow_comp', comp, promotes=['*'])