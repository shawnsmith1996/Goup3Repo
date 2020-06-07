from openmdao.api import Group
from openmdao.api import IndepVarComp

from weights.FuelWeightRatio import FuelWeightRatio
from weights.gross_weight import GrossWeight
from weights.empty_weight import Empty_Weight


from weights.w_weight import w_weight_comp
from weights.t_weight import h_tailweight_comp
from weights.t_weight import v_tailweight_comp
from weights.f_weight import f_weight_comp


class weightGroup(Group):


    def setup(self):
        comp = FuelWeightRatio()
        self.add_subsystem('FuelWeightRatio',comp,promotes=['*'])

        comp = GrossWeight()
        self.add_subsystem('GrossWeight',comp,promotes=['*'])

        comp = Empty_Weight()
        self.add_subsystem('Empty_Weight',comp,promotes=['*'])




        comp = w_weight_comp(N=3.,tc=0.3,AR=9.,sweep=30.)
        self.add_subsystem('wing_weight',comp,promotes=['*'])

        comp = h_tailweight_comp(N=3.,lift_tail=85.,htail_aspect_ratio=4.,sweepht=27.)
        self.add_subsystem('h_tail_weight',comp,promotes=['*'])

        comp = v_tailweight_comp(N=3.,lift_tail=85.,vtail_aspect_ratio=4.,sweepvt=27.,tc=0.3)
        self.add_subsystem('v_tail_weight',comp,promotes=['*'])

        comp = f_weight_comp(N=3.,L=205.,lift_drag=17.,fuselage_area=15030.,sweep=30.,taper=0.3)
        self.add_subsystem('fuselage_weight',comp,promotes=['*'])

