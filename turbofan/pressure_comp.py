from __future__ import print_function
import numpy as np

from lsdo_utils.api import ArrayExplicitComponent



class PressureComp(ArrayExplicitComponent):
    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        self.add_input('altitude_km')
        self.add_output('pressure_MPa')
        self.declare_partials('pressure_MPa', 'altitude_km')
        


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
        #### Presssure COeef
        tmp1 = 1 - L * h_lower / T0
        tmp2 = np.exp(-g * epsilon / (R * T1))
        pressure_rhs = np.array([
            p0 * tmp1 ** g_L_R,
            p1 * tmp2,
            (-p0 * g_L_R * (L / T0) * tmp1 ** (g_L_R - 1)),
            (p1 * -g / (R * T1) * tmp2)])
        pressure_coeffs = np.linalg.solve(tropopause_matrix, pressure_rhs)
        ## Mask
        tropos_mask = h_m <= h_lower
        strato_mask = h_m >  h_upper
        smooth_mask = np.logical_and(~tropos_mask, ~strato_mask)
        ## Calc
        a, b, c, d = pressure_coeffs

        p_Pa = np.zeros(h_m.shape, dtype=h_m.dtype)
        p_Pa += tropos_mask * (p0 * (1 - L * h_m / T0) ** g_L_R)
        p_Pa += strato_mask * (p1 * np.exp(-g * (h_m - h_trans) / (R * T1)))
        p_Pa += smooth_mask * (a * h_m ** 3 + b * h_m ** 2 + c * h_m + d)



        outputs['pressure_MPa'] = p_Pa / 1e6

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
        ## Transpose Matrix
        h_lower = h_trans - epsilon
        h_upper = h_trans + epsilon
        tropopause_matrix = np.array([
            [h_lower ** 3, h_lower ** 2, h_lower, 1],
            [h_upper ** 3, h_upper ** 2, h_upper, 1],
            [3 * h_lower ** 2, 2 * h_lower, 1, 0],
            [3 * h_upper ** 2, 2 * h_upper, 1, 0],
        ])
        #### Presssure COeef
        tmp1 = 1 - L * h_lower / T0
        tmp2 = np.exp(-g * epsilon / (R * T1))
        pressure_rhs = np.array([
            p0 * tmp1 ** g_L_R,
            p1 * tmp2,
            (-p0 * g_L_R * (L / T0) * tmp1 ** (g_L_R - 1)),
            (p1 * -g / (R * T1) * tmp2)])
        pressure_coeffs = np.linalg.solve(tropopause_matrix, pressure_rhs)
        ## Mask
        tropos_mask = h_m <= h_lower
        strato_mask = h_m >  h_upper
        smooth_mask = np.logical_and(~tropos_mask, ~strato_mask)

        ## Calc
        a, b, c, _ = pressure_coeffs

        derivs = np.zeros(h_m.shape, dtype=h_m.dtype)
        derivs += tropos_mask * (p0 * g_L_R * (-L / T0) * (1 - L * h_m / T0)** (g_L_R - 1))
        derivs += strato_mask * (p1 * (-g/(R * T1))
        *np.exp(g * h_trans / (R * T1)) * np.exp(-g * h_m / (R * T1)))
        derivs += smooth_mask * (3 * a * h_m ** 2 + 2 * b * h_m + c)

        partials['pressure_MPa', 'altitude_km'] = derivs * 1e3 / 1e6