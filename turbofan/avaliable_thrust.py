
import numpy as np

from openmdao.api import ExplicitComponent


class Avaliable_Thrust(ExplicitComponent):


    def setup(self):
        self.add_input('thrust_ratio')
        self.add_input('zerospeed_thrust')
        self.add_output('avaliable_thrust')

        self.declare_partials('avaliable_thrust', 'thrust_ratio')
        self.declare_partials('avaliable_thrust', 'zerospeed_thrust')

    def compute(self, inputs, outputs):
        thrust_ratio=inputs['thrust_ratio']
        zerospeed_thrust=inputs['zerospeed_thrust']

        outputs['avaliable_thrust'] = (thrust_ratio * zerospeed_thrust)
    
    
#    def Thrust(self, inputs, outputs):
#        comp = PowerCombinationComp(
#            shape=shape,
#            out_name='thrust',
#            powers_dict=dict(
#                thrust_ratio=1.,
#                zero_spd_thrust=1.,
#            ),
#        )

    def compute_partials(self, inputs, partials):

        thrust_ratio=inputs['thrust_ratio']
        zerospeed_thrust=inputs['zerospeed_thrust']

        partials['avaliable_thrust', 'thrust_ratio'] = thrust_ratio
        partials['avaliable_thrust', 'zerospeed_thrust'] = zerospeed_thrust

