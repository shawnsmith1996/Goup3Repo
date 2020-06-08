import numpy as np

from openmdao.api import ExplicitComponent


class w_weight_comp(ExplicitComponent):

    def initialize(self):
        self.options.declare('N', types=float)
        self.options.declare('tc', types=float)
        self.options.declare('AR', types=float)
        self.options.declare('sweep', types=float)

    def setup(self):
        self.add_input('gross_weight')
        self.add_input('wing_area')
        self.add_output('wing_weight')

        self.declare_partials('wing_weight', 'gross_weight')
        self.declare_partials('wing_weight', 'wing_area')

    def compute(self, inputs, outputs):
        N = self.options['N']
        tc = self.options['tc']
        AR = self.options['AR']
        sweep = self.options['sweep']

        gross_weight = inputs['gross_weight']
        wing_area = inputs['wing_area']

        cosSweep = np.cos(sweep * np.pi / 180)

        outputs['wing_weight'] = 0.0051 * gross_weight ** 0.557 * N ** 0.557 * wing_area ** 0.649 * AR ** 0.5 * tc ** -0.4 * cosSweep ** -1 * 0.1 ** 0.1 * wing_area ** 0.1

    def compute_partials(self, inputs, partials):
        N = self.options['N']
        tc = self.options['tc']
        AR = self.options['AR']
        sweep = self.options['sweep']

        gross_weight = inputs['gross_weight']
        wing_area = inputs['wing_area']

        cosSweep = np.cos(sweep * np.pi / 180)

        partials['wing_weight', 'gross_weight'] = 0.0051 * 0.557 * gross_weight ** -0.443 * N ** 0.557 * wing_area ** 0.649 * AR ** 0.5 * tc ** -0.4 * cosSweep ** -1 * 0.1 ** 0.1 * wing_area ** 0.1
        partials['wing_weight', 'wing_area'] = 0.0051 * gross_weight ** 0.557 * N ** 0.557 * 0.649 * wing_area ** -0.351 * AR ** 0.5 * tc ** -0.4 * cosSweep ** -1 * 0.1 ** 0.1 * 0.1 * wing_area ** -0.9