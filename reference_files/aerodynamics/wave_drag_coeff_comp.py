import numpy as np

from lsdo_utils.api import ArrayExplicitComponent


class WaveDragCoeffComp(ArrayExplicitComponent):

    def setup(self):
        self.add_input('M_inf')
        self.add_input('critical_mach_number')
        self.add_output('CDw')

        self.declare_partials('CDw', 'M_inf')
        self.declare_partials('CDw', 'critical_mach_number')

    def compute(self, inputs, outputs):
        d_mach = inputs['M_inf'] - inputs['critical_mach_number']
        d_mach *= d_mach > 0.

        outputs['CDw'] = 20. * d_mach ** 4

    def compute_partials(self, inputs, partials):
        d_mach = (inputs['M_inf'] - inputs['critical_mach_number']).flatten()
        d_mach *= d_mach > 0.

        partials['CDw', 'M_inf'] = 80. * d_mach ** 3
        partials['CDw', 'critical_mach_number'] = -80. * d_mach ** 3

