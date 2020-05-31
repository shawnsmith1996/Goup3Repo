#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import unittest

from turbofan.specific_fuel_consum import specific_fuel_consum
from openmdao.api import Problem
from openmdao.utils.assert_utils import assert_check_partials


class TestSpecificFuelConsumComp(unittest.TestCase):

    def test_component_and_derivatives(self):
        prob = Problem()
        prob.model = Specific_Fuel_Consum()
        prob.setup()
        prob.run_model()

        data = prob.check_partials(out_stream=None)
        assert_check_partials(data, atol=1.e-3, rtol=1.e-3)


if __name__ == '__main__':
    unittest.main()

