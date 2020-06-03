import numpy as np
from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver

from cost.fl_comp import FlyawayComp
from cost.fuel_comp import FuelComp
from cost.main_comp import MainComp
from cost.rdte_comp import RDTEComp

prob = Problem()

model = Group()

comp = IndepVarComp()
comp.add_output('EN', val=500 * 2)
comp.add_output('FTA', val=3)
comp.add_output('mass_flow_rate', val=0.83)
comp.add_output('Q', val=500)
comp.add_output('Tinlet', val = 3303)
comp.add_output('sealevel_thrust', val=74400)
comp.add_output('velocity_ms', val=466)
comp.add_output('We', val=187346)
comp.add_output('Wfr', val=34300)

model.add_subsystem('inputs_comp', comp, promotes=['*'])

comp = FlyawayComp()
model.add_subsystem('fl_comp', comp, promotes=['*'])

comp = FuelComp()
model.add_subsystem('fuel_comp', comp, promotes=['*'])

comp = MainComp()
model.add_subsystem('main_comp', comp, promotes=['*'])

comp = RDTEComp()
model.add_subsystem('rdte_comp', comp, promotes=['*'])

prob.model = model

prob.setup()
prob.run_model()

prob.check_partials(compact_print=True)