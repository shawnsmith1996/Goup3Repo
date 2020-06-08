import openmdao.api as om
from openmdao.api import Group
from openmdao.api import IndepVarComp

from weights.group_weight import weightGroup
from cost.group_cost import CostGroup

class weight_cost(Group):

    def setup(self):
        group = weightGroup()
        self.add_subsystem('weight',group,promotes=['*'])
        group = CostGroup()
        self.add_subsystem('cost',group,promotes=['*'])
        self.nonlinear_solver=om.NonLinearBlockGS(rtol=1.0e-5)