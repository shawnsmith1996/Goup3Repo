# maximize L/D
# w.r.t. alpha
# s.t. CL >= CL*

# Model inputs: alpha, CL0, CD0, AR
# Model outputs: (L/D), CL

# Models:
# Component 1: alpha, CL0, CD0, AR
# Component 2: CL = CLa * alpha + CL0
# Component 3: CDi = CL^2 / (pi e AR)
# Component 4: CD = CD0 + CDi
# Component 5: L/D = CL/CD

import numpy as np
from openmdao.api import Problem, Group, IndepVarComp, ExecComp, ScipyOptimizeDriver

from turbofan.pressure_comp import PressureComp
from turbofan.temperature_comp import TemperatureComp
from turbofan.density_comp import DensityComp


from turbofan.mach_num import Mach_Num

from turbofan.avaliable_thrust import Avaliable_Thrust
from turbofan.thrust import Thrust
from turbofan.mass_flow import Mass_Flow_Rate
from turbofan.specific_fuel_consum import Specific_Fuel_Consum
from turbofan.thrust_ratio import Thrust_Ratio



prob = Problem()

model = Group()

comp = IndepVarComp()
comp.add_output('altitude_km', val=0.04)
comp.add_output('sealevel_thrust', val=0.04)

comp.add_output('velocity_ms', val=0.015)

comp.add_output('B', val=0.2)
comp.add_output('k', val=0.2)

comp.add_output('A', val=8.)
comp.add_output('n', val=8.)
model.add_subsystem('inputs_comp', comp, promotes=['*'])


################ Constants #############
comp = IndepVarComp()
comp.add_output('sealevel_density', val=1.225)
comp.add_output('throttle', val=1.)
comp.add_output('thrust_specific_fuel_consumption', val=0.61)
model.add_subsystem('constants', comp, promotes=['*'])

############## System Section Bottom #########
comp = PressureComp()
model.add_subsystem('pressure_comp', comp, promotes=['*'])

comp = TemperatureComp()
model.add_subsystem('temperature_comp', comp, promotes=['*'])

comp = DensityComp() 
model.add_subsystem('density_comp', comp, promotes=['*'])
## Atmosphere above

comp= Mach_Num()
model.add_subsystem('mach_comp', comp, promotes=['*'])
## Mach num calc above

## Thrust Equations
comp = Avaliable_Thrust()
model.add_subsystem('avaliable_thrust_comp', comp, promotes=['*'])

comp = Thrust()
model.add_subsystem('thrust_comp', comp, promotes=['*'])

comp = Mass_Flow_Rate()
model.add_subsystem('mass_flow_comp', comp, promotes=['*'])

comp = Specific_Fuel_Consum()
model.add_subsystem('specific_fuel_consum_comp', comp, promotes=['*'])

comp = Thrust_Ratio()
model.add_subsystem('thrust_ratio_comp', comp, promotes=['*'])

#comp = ExecComp('CD = CD0 + CDi')
#model.add_subsystem('cd_comp', comp, promotes=['*'])

#comp = ExecComp('LD = mass_flow_rate')
#comp.add_objective('LD', scaler=-1.)
#model.add_subsystem('ld_comp', comp, promotes=['*'])

prob.model = model

#prob.driver = ScipyOptimizeDriver()
#prob.driver.options['optimizer'] = 'SLSQP'
#prob.driver.options['tol'] = 1e-15
#prob.driver.options['disp'] = True

prob.setup()
prob.run_model()
#prob.run_driver()

prob.check_partials(compact_print=True)

#print('sealevel_thrust', prob['sealevel_thrust'])
#print('density', prob['density'])
#print('sealevel_density', prob['sealevel_density'])
#print('avaliable_thrust', prob['avaliable_thrust'])

#print('throttle', prob['throttle'])
#print('thrust', prob['thrust'])

#print('mass_flow_rate', prob['mass_flow_rate'])

#print('B', prob['B'])
#print('k', prob['k'])
#print('M_inf', prob['M_inf'])
#print('specific_fuel_consum', prob['specific_fuel_consum'])

#print('A', prob['A'])
#print('n', prob['n'])
#print('thrust_ratio', prob['thrust_ratio'])



# Visualization: ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 

#alpha_opt = prob['alpha'][0]

#num = 100
#alpha_sweep = np.linspace(-0.1, 0.2, num)
#CL_list = np.empty(num)
#CD_list = np.empty(num)

#for ind in range(num):
#    prob['alpha'] = alpha_sweep[ind]
#    prob.run_model()
#    CL_list[ind] = prob['CL'][0]
#    CD_list[ind] = prob['CD'][0]

#prob['alpha'] = alpha_opt
#prob.run_model()
#CL_opt = prob['CL'][0]
#CD_opt = prob['CD'][0]

#import matplotlib.pyplot as plt

#plt.plot(
#    [0., CD_opt],
#    [0., CL_opt],
#)
#plt.plot(CD_list, CL_list)
#plt.xlabel('CD')
#plt.ylabel('CL')
#plt.show()