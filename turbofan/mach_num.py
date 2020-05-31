

from openmdao.api import ExplicitComponent
import numpy as np
from turbofan.constants import R,gamma
class Mach_Num(ExplicitComponent):

        
    def setup(self):
        self.add_input('velocity_ms')
        self.add_input('temperature')
        self.add_output('M_inf')
        
        self.declare_partials('M_inf', 'velocity_ms')
        self.declare_partials('M_inf', 'temperature')

    def compute(self, inputs, outputs):
        velocity=inputs['velocity_ms']
        temperature=inputs['temperature']

        outputs['M_inf'] = velocity / (np.sqrt(gamma*temperature*R))
        
#         comp = PowerCombinationComp(
#            shape=shape,
#            coeff=1/np.sqrt(gamma*R)
#            out_name='M_inf',
#            powers_dict=dict(
#                velocity_ms=1.,
#                temperature=-0.5.,
#            )
#        )

    def compute_partials(self, inputs, partials):

        velocity=inputs['velocity_ms']
        temperature=inputs['temperature']

        partials['M_inf', 'velocity_ms'] =1 / (np.sqrt(gamma*temperature*R))
        partials['M_inf', 'temperature'] =(velocity / (np.sqrt(gamma*R)))*(1/(2*np.sqrt(temperature**3)))
        


