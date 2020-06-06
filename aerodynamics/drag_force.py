import numpy as np

from openmdao.api import ExplicitComponent

class DragForce(ExplicitComponent):
    def setup(self):
        self.add_input('velocity_ms')
        self.add_input('density')
        self.add_input('CD')
        self.add_output('drag')

        self.declare_partials('drag', 'velocity_ms')
        self.declare_partials('drag', 'density')
        self.declare_partials('drag', 'CD')

    def compute(self, inputs, outputs):
        V = inputs['velocity_ms']
        rho = inputs['density']
        CD = inputs['CD']

        outputs['drag'] = 1/2 * rho * CD * V **2

    def compute_partials(self, inputs, partials):
        V = inputs['velocity_ms']
        rho = inputs['density']
        CD = inputs['CD']

        partials['drag', 'velocity_ms'] = rho * CD * V
        partials['drag', 'density'] = 1/2 * CD * V **2
        partials['drag', 'CD'] = 1/2 * rho * V **2