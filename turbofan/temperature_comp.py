from __future__ import print_function
import numpy as np

from lsdo_utils.api import ArrayExplicitComponent


class TemperatureComp(ArrayExplicitComponent):

    def setup(self):
        self.add_input('altitude_km')
        self.add_output('temperature')
        self.declare_partials('temperature', 'altitude_km')

    def compute(self, inputs, outputs):
        epsilon = 500
        h_trans = 11000
        T0 = 288.16
        T1 = 216.65
        T2 = 273.15
        Ts = 110.4
        L = 6.5e-3
        R = 287.058
        p0 = 101325
        p1 = 22632
        g = 9.81
        gamma = 1.4
        mu2 = 1.716e-5
        h_m = inputs['altitude_km'] * 1e3

        g_L_R = g / L / R
        ## Transpose Matrix
        h_lower = h_trans - epsilon
        h_upper = h_trans + epsilon
        tropopause_matrix = np.array([
            [h_lower ** 3, h_lower ** 2, h_lower, 1],
            [h_upper ** 3, h_upper ** 2, h_upper, 1],
            [3 * h_lower ** 2, 2 * h_lower, 1, 0],
            [3 * h_upper ** 2, 2 * h_upper, 1, 0],
        ])
        ## Temp Coeef
        temp_rhs = np.array([
            T0 - L * h_lower,
            T1,
            -L,
            0,
        ])
        temp_coeffs = np.linalg.solve(tropopause_matrix, temp_rhs)
        ## Mask
        tropos_mask = h_m <= h_lower
        strato_mask = h_m >  h_upper
        smooth_mask = np.logical_and(~tropos_mask, ~strato_mask)
        ### Calc
        a, b, c, d = temp_coeffs
        temp_K = np.zeros(h_m.shape, dtype=h_m.dtype)
        temp_K += tropos_mask * (T0 - L * h_m)
        temp_K += strato_mask * T1
        temp_K += smooth_mask * (a * h_m ** 3 + b * h_m ** 2 + c * h_m + d)
        outputs['temperature'] = temp_K

    def compute_partials(self, inputs, partials):
        epsilon = 500
        h_trans = 11000
        T0 = 288.16
        T1 = 216.65
        T2 = 273.15
        Ts = 110.4
        L = 6.5e-3
        R = 287.058
        p0 = 101325
        p1 = 22632
        g = 9.81
        gamma = 1.4
        mu2 = 1.716e-5
        h_m = inputs['altitude_km'] * 1e3

        g_L_R = g / L / R
        ## Matrix
        h_lower = h_trans - epsilon
        h_upper = h_trans + epsilon
        tropopause_matrix = np.array([
            [h_lower ** 3, h_lower ** 2, h_lower, 1],
            [h_upper ** 3, h_upper ** 2, h_upper, 1],
            [3 * h_lower ** 2, 2 * h_lower, 1, 0],
            [3 * h_upper ** 2, 2 * h_upper, 1, 0],
        ])
        ## Temp Coeef
        temp_rhs = np.array([
            T0 - L * h_lower,
            T1,
            -L,
            0,
        ])
        temp_coeffs = np.linalg.solve(tropopause_matrix, temp_rhs)
        ## Mask
        tropos_mask = h_m <= h_lower
        strato_mask = h_m >  h_upper
        smooth_mask = np.logical_and(~tropos_mask, ~strato_mask)
        ### Calc
        a, b, c, _ = temp_coeffs
        derivs = np.zeros(h_m.shape, dtype=h_m.dtype)
        derivs += tropos_mask * -L
        derivs += smooth_mask * (3 * a * h_m ** 2 + 2 * b * h_m + c)

        partials['temperature', 'altitude_km'] = derivs * 1e3