import numpy as np
from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver

from cost.fl_comp import FlyawayComp
from cost.fuel_comp import FuelComp
from cost.main_comp import MainComp
from cost.rdte_comp import RDTEComp

prob = Problem()

model = Group()

comp = IndepVarComp()
comp.add_output('velocity_ms', val=466)
comp.add_output('We', val=187346)
comp.add_output('Wfr', val=34300)

model.add_subsystem('inputs_comp', comp, promotes=['*'])


comp = IndepVarComp()
comp.add_output('MHFH', val=10) ## Maintaince Hour Per Flight Hour
comp.add_output('M_max', val=0.83) ## Engine max mach number
comp.add_output('T_max', val=74400) ## Engine max Thrust
comp.add_output('EN', val=500 * 2) ## Engine Number
comp.add_output('FTA', val=3) ###FTA flight test
comp.add_output('Q', val=500) ### Less number production
comp.add_output('Tinlet', val = 3303) ## Turbine inlet temperature
prob.model.add_subsystem('constants', comp, promotes=['*'])


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