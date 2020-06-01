from __future__ import print_function
import numpy as np

from lsdo_utils.api import ArrayExplicitComponent




class DensityComp(ArrayExplicitComponent):

    def setup(self):
        self.add_input('pressure_MPa')
        self.add_input('temperature')
        self.add_output('density')
        self.declare_partials('density', 'pressure_MPa')
        self.declare_partials('density', 'temperature')

    def compute(self, inputs, outputs):
        R=287.058
        p_Pa = inputs['pressure_MPa'] * 1e6
        temperature = inputs['temperature']

        outputs['density'] = p_Pa / R / temperature

    def compute_partials(self, inputs, partials):
        R=287.058
        p_Pa = inputs['pressure_MPa'].flatten() * 1e6
        temperature = inputs['temperature'].flatten()

        partials['density', 'pressure_MPa'] = 1. / R / temperature * 1e6
        partials['density', 'temperature'] = -p_Pa / R / temperature ** 2