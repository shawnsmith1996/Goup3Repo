import numpy as np

from openmdao.api import ScipyOptimizeDriver
try:
    from openmdao.api import pyOptSparseDriver
except:
    pyOptSparseDriver = None

from beam_group import BeamGroup

from lsdo_viz.api import Problem


E = 1.
L = 1.
b = 0.1
volume = 0.01

num_elements = 50

prob = Problem(model=BeamGroup(E=E, L=L, b=b, volume=volume, num_elements=num_elements))

prob.driver = ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'
prob.driver.options['tol'] = 1e-9
prob.driver.options['disp'] = True

# if pyOptSparseDriver:
#     prob.driver = pyOptSparseDriver()
#     prob.driver.options['optimizer'] = 'SNOPT'

prob.setup()

prob.run()