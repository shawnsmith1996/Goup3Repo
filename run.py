import numpy as np
import openmdao.api as om
from openmdao.api import Problem, IndepVarComp, ScipyOptimizeDriver

from group_structures import StructuresGroup
from group_thrust import TurbofanGroup
from group_weight import weightGroup
from group_cost import CostGroup

prob = Problem()
comp = IndepVarComp()
comp.add_output('altitude_km', val=4400,units='m')
comp.add_output('velocity_ms', val=248.136,units='m/s')
comp.add_output('chord',val=0.1, units='m')

prob.model.add_subsystem('opt_input_comp', comp, promotes=['*'])


comp = IndepVarComp()
comp.add_output('wing_span',val=44, units='m')
comp.add_output('drag', val=34400, units='kN')
comp.add_input('LD',val=1) #lift over drag
comp.add_output('wing_area',val=17346,units='m**2')
comp.add_output('horizontal_tail_area',val=17346, units='m')
comp.add_output('bw',val=17346)## whats this?
prob.model.add_subsystem('inputs_comp', comp, promotes=['*'])


comp = IndepVarComp()
comp.add_input('R',val=700,units='NM') #range
comp.add_output('payload_weight',val=4400, units='kg')
comp.add_output('crew_weight',val=4400, units='kg')
comp.add_output('empty_weight_fraction',val=0.4)

comp.add_output('A', val=8.) ## still need to fix these values #Modeling Constants
comp.add_output('B', val=0.2)#Modeling Constants
comp.add_output('n', val=8.)#Modeling Constants
comp.add_output('k', val=0.2) #Modeling Constants

comp.add_output('MHFH', val=10) ## Maintaince Hour Per Flight Hour
comp.add_output('M_max', val=0.83) ## Engine max mach number
comp.add_output('T_max', val=74400, units='kN') ## Engine max Thrust
comp.add_output('EN', val=500 * 2) ## Engine Number
comp.add_output('FH', val=3500, units='h') ###flight hour
comp.add_output('FTA', val=3) ###FTA flight test
comp.add_output('Q', val=500) ### Less number production
comp.add_output('Tinlet', val = 3303, units='K') ## Turbine inlet temperature

prob.model.add_subsystem('constants', comp, promotes=['*'])


group = StructuresGroup()
prob.model.add_subsystem('structure_group', group, promotes=['*'])
group = TurbofanGroup()
prob.model.add_subsystem('propulsion_group', group, promotes=['*'])
group = weightGroup()
prob.model.add_subsystem('weight_group', group, promotes=['*'])
group = CostGroup()
prob.model.add_subsystem('cost_group', group, promotes=['*'])

#prob.driver = ScipyOptimizeDriver()
#prob.driver.options['optimizer'] = 'SLSQP'
#prob.driver.options['tol'] = 1e-15
#prob.driver.options['disp'] = True

prob.setup()
prob.run_model()
#prob.run_driver()

prob.check_partials(compact_print=True)