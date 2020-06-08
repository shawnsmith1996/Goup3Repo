import numpy as np

from openmdao.api import ExplicitComponent


class h_tailweight_comp(ExplicitComponent):

    def initialize(self):
        self.options.declare('N', types=float)
        self.options.declare('lift_tail', types=float)
        self.options.declare('htail_aspect_ratio', types=float)
        self.options.declare('sweepht', types=float)
    

    def setup(self):
        self.add_input('gross_weight')
        self.add_input('horizontal_tail_area')
        self.add_output('horizontial_tail_weight')

        self.declare_partials('horizontial_tail_weight', 'gross_weight')
        self.declare_partials('horizontial_tail_weight', 'horizontal_tail_area')

    def compute(self, inputs, outputs):
        N = self.options['N']
        lift_tail = self.options['lift_tail']
        htail_aspect_ratio = self.options['htail_aspect_ratio']
        sweepht = self.options['sweepht']
       

        gross_weight = inputs['gross_weight']
        horizontal_tail_area = inputs['horizontal_tail_area']

        cosSweepht = np.cos(sweepht * np.pi / 180)
        Ky = 0.3 * lift_tail

        outputs['horizontial_tail_weight'] = 0.0379 * 1.2 ** -0.25 * gross_weight ** 0.639 * N ** 0.1 * horizontal_tail_area ** 0.75 * lift_tail ** -1 * Ky ** 0.704 * cosSweepht ** -1 * htail_aspect_ratio ** 0.166

    def compute_partials(self, inputs, partials):
        N = self.options['N']
        lift_tail = self.options['lift_tail']
        htail_aspect_ratio = self.options['htail_aspect_ratio']
        sweepht = self.options['sweepht']

        gross_weight = inputs['gross_weight']
        horizontal_tail_area = inputs['horizontal_tail_area']

        cosSweepht = np.cos(sweepht * np.pi / 180)
        Ky = 0.3 * lift_tail

        partials['horizontial_tail_weight', 'gross_weight'] = 0.0379 * 1.2 ** -0.25 * 0.639 * gross_weight ** -0.361 * N ** 0.1 * horizontal_tail_area ** 0.75 * lift_tail ** -1 * Ky ** 0.704 * cosSweepht ** -1 * htail_aspect_ratio ** 0.166
        partials['horizontial_tail_weight', 'horizontal_tail_area'] = 0.0379 * 1.2 ** -0.25 * gross_weight ** 0.639 * N ** 0.1 * 0.75 * horizontal_tail_area ** -0.25 * lift_tail ** -1 * Ky ** 0.704 * cosSweepht ** -1 * htail_aspect_ratio ** 0.166

class v_tailweight_comp(ExplicitComponent):

    def initialize(self):
        self.options.declare('N', types=float)
        self.options.declare('lift_tail', types=float)
        self.options.declare('vtail_aspect_ratio', types=float)
        self.options.declare('sweepvt', types=float)
        self.options.declare('tc',types=float)
    

    def setup(self):
        self.add_input('gross_weight')
        self.add_input('horizontal_tail_area')
        self.add_output('vertical_tail_weight')

        self.declare_partials('vertical_tail_weight', 'gross_weight')
        self.declare_partials('vertical_tail_weight', 'horizontal_tail_area')

    def compute(self, inputs, outputs):
        N = self.options['N']
        lift_tail = self.options['lift_tail']
        vtail_aspect_ratio = self.options['vtail_aspect_ratio']
        sweepvt = self.options['sweepvt']
        tc = self.options['tc']
       

        gross_weight = inputs['gross_weight']
        horizontal_tail_area = inputs['horizontal_tail_area']

        cosSweepvt = np.cos(sweepvt * np.pi / 180)
        Kz = lift_tail

        outputs['vertical_tail_weight'] = 0.0026 * gross_weight ** 0.556 * N ** 0.536 * horizontal_tail_area ** 0.5 * lift_tail ** -0.5 * Kz ** 0.875 * cosSweepvt ** -1 * vtail_aspect_ratio ** 0.35 * tc ** -0.5

    def compute_partials(self, inputs, partials):
        N = self.options['N']
        lift_tail = self.options['lift_tail']
        vtail_aspect_ratio = self.options['vtail_aspect_ratio']
        sweepvt = self.options['sweepvt']
        tc = self.options['tc']

        gross_weight = inputs['gross_weight']
        horizontal_tail_area = inputs['horizontal_tail_area']

        cosSweepvt = np.cos(sweepvt * np.pi / 180)
        Kz = lift_tail

        partials['vertical_tail_weight', 'gross_weight'] = 0.0026 * 0.556 * gross_weight ** -0.444 * N ** 0.536 * horizontal_tail_area ** 0.5 * lift_tail ** -0.5 * Kz ** 0.875 * cosSweepvt ** -1 * vtail_aspect_ratio ** 0.35 * tc ** -0.5
        partials['vertical_tail_weight', 'horizontal_tail_area'] = 0.0026 * gross_weight ** 0.556 * N ** 0.536 * 0.5 * horizontal_tail_area ** -0.5 * lift_tail ** -0.5 * Kz ** 0.875 * cosSweepvt ** -1 * vtail_aspect_ratio ** 0.35 * tc ** -0.5
