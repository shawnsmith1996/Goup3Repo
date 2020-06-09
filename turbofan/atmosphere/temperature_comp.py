from __future__ import print_function
import numpy as np

from lsdo_utils.api import ArrayExplicitComponent
from turbofan.atmosphere.atmosph_utils import \
    get_mask_arrays, compute_temps, compute_temp_derivs


class TemperatureComp(ArrayExplicitComponent):

    def setup(self):
        self.add_input('altitude')
        self.add_output('temperature')
        self.declare_partials('temperature', 'altitude_km')

    def compute(self, inputs, outputs):
        h_m = inputs['altitude_km'] * 1e3

        self.mask_arrays = get_mask_arrays(h_m)

        temp_K = compute_temps(h_m, *self.mask_arrays)

        outputs['temperature'] = temp_K

    def compute_partials(self, inputs, partials):
        h_m = inputs['altitude_km'] * 1e3
        derivs = compute_temp_derivs(h_m, *self.mask_arrays).flatten()

        partials['temperature', 'altitude_km'] = derivs * 1e3