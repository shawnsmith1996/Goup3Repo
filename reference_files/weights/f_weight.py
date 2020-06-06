import numpy as np

from openmdao.api import ExplicitComponent


class f_weight_comp(ExplicitComponent):

    def initialize(self):
        self.options.declare('N', types=float)
        self.options.declare('L', types=float)
        self.options.declare('lift_drag', types=float)
        self.options.declare('fuselage_area', types=float)
        self.options.declare('sweep', types=float)
        self.options.declare('taper', types=float)

    def setup(self):
        self.add_input('gross_weight')
        self.add_input('bw')
        self.add_output('fuselage_weight')

        self.declare_partials('fuselage_weight', 'gross_weight')

    def compute(self, inputs, outputs):
        N = self.options['N']
        L = self.options['L']
        lift_drag = self.options['lift_drag']
        fuselage_area = self.options['fuselage_area']
        sweep = self.options['sweep']
        taper = self.options['taper']

        gross_weight = inputs['gross_weight']
        bw = inputs['bw']

        Kws = 0.75 * (1 + 2 * taper) / (1 + taper) * bw * np.tan(sweep / L * (np.pi / 180))

        outputs['fuselage_weight'] = 0.328 * 1.12 * gross_weight ** 0.5 * N ** 0.5  * L ** 0.25 * fuselage_area ** 0.302 * (1 + Kws) ** 0.04 * lift_drag ** 0.1

    def compute_partials(self, inputs, partials):
        N = self.options['N']
        L = self.options['L']
        lift_drag = self.options['lift_drag']
        fuselage_area = self.options['fuselage_area']
        sweep = self.options['sweep']
        taper = self.options['taper']

        gross_weight = inputs['gross_weight']
        bw = inputs['bw']

        Kws = 0.75 * (1 + 2 * taper) / (1 + taper) * bw * np.tan(sweep / L * (np.pi / 180))

        partials['fuselage_weight', 'gross_weight'] = 0.328 * 1.12 * 0.5 * gross_weight ** -0.5 * N ** 0.5 * L ** 0.25 * fuselage_area ** 0.302 * (1 + Kws) ** 0.04 * lift_drag ** 0.1

       