from openmdao.api import Problem, ScipyOptimizeDriver, pyOptSparseDriver

from openmdao.test_suite.test_examples.beam_optimization.multipoint_beam_group import MultipointBeamGroup

E = 1.
L = 0.5
b = 0.1
h = 0.1
volume = L * b * h

num_cp = 4
num_elements = 5 * num_cp
num_load_cases = 1

prob = Problem(
    model=MultipointBeamGroup(
        E=E, L=L, b=b, volume=volume,
        num_elements=num_elements, num_cp=num_cp,
        num_load_cases=num_load_cases,
    ),
)

prob.driver = ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'
prob.driver.options['tol'] = 1e-9
prob.driver.options['disp'] = True

prob.driver = pyOptSparseDriver()
prob.driver.options['optimizer'] = 'SNOPT'

# prob.model.approx_totals()

prob.setup()

prob.run_driver()