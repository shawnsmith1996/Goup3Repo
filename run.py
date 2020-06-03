from openmdao.api import Problem, IndepVarComp, ScipyOptimizeDriver
from weightGroup import weightCompGroup
from thrust_group import TurbofanGroup
from cost_group import CostGroup


prob = Problem()

comp = IndepVarComp()
comp.add_output('altitude_km', val=0.04)
comp.add_output('drag', val=0.04)
comp.add_output('sealevel_thrust', val=0.04)
comp.add_output('velocity_ms', val=0.015)

comp.add_output('k', val=0.2)

comp.add_output('EN', val=500 * 2)
comp.add_output('FTA', val=3)
comp.add_output('Q', val=500)
comp.add_output('Tinlet', val = 3303)
comp.add_output('We', val=187346)
comp.add_output('Wfr', val=34300)

comp.add_input('W0',val=500)
comp.add_input('Bw',val=500)
comp.add_input('Wl',val=500)
comp.add_input('Sht',val=500)
comp.add_input('Svt',val=500)
prob.model.add_subsystem('inputs_comp', comp, promotes=['*'])

comp = IndepVarComp()
comp.add_output('A', val=8.) ## still need to fix these values
comp.add_output('B', val=0.2)
comp.add_output('n', val=8.)
prob.model.add_subsystem('constants', comp, promotes=['*'])


group = weightCompGroup()
prob.model.add_subsystem('weight_group', group, promotes=['*'])
group = TurbofanGroup()
prob.model.add_subsystem('propulsion_group', group, promotes=['*'])
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