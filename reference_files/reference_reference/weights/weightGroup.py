from openmdao.api import Group
from openmdao.api import IndepVarComp

from weights.w_weight import w_weight_comp
from weights.t_weight import h_tailweight_comp
from weights.t_weight import v_tailweight_comp
from weights.f_weight import f_weight_comp


class weightGroup(Group):


    def setup(self):
        comp = w_weight_comp()
        self.add_subsystem('wing_weight',comp,promotes=['*'])

        comp = h_tailweight_comp()
        self.add_subsystem('h_tail_weight',comp,promotes=['*'])

        comp = v_tailweight_comp()
        self.add_subsystem('v_tail_weight',comp,promotes=['*'])

        comp = f_weight_comp()
        self.add_subsystem('fuselage_weight',comp,promotes=['*'])

