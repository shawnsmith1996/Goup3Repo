#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

from openmdao.api import ExplicitComponent


class Thottled_Thrust(ExplicitComponent):


    def setup(self):
        self.add_input('sealevel_thrust')
        self.add_input('throttle')
        self.add_input('avaliable_thrust')
        self.add_output('thottled_thrust')

        self.declare_partials('thottled_thrust', 'sealevel_thrust')
        self.declare_partials('thottled_thrust', 'avaliable_thrust')

    def compute(self, inputs, outputs):
        sealevel_thrust=inputs['sealevel_thrust']
        avaliable_thrust=inputs['avaliable_thrust']
        if sealevel_thrust < avaliable_thrust:
            throttle=1.
        elif avaliable_thrust < 0 or sealevel_thrust < 0:
            throttle=0.
        else:
            throttle=avaliable_thrust/sealevel_thrust

        outputs['thottled_thrust'] = (throttle * avaliable_thrust)
    
    
#    def Thrust(self, inputs, outputs):
#        comp = PowerCombinationComp(
#            shape=shape,
#            out_name='zero_spd_thrust',
#            powers_dict=dict(
#                throttle=1.,
#                available_thrust=1.,
#            ),
#        )

    def compute_partials(self, inputs, partials):

        sealevel_thrust=inputs['sealevel_thrust']
        avaliable_thrust=inputs['avaliable_thrust']
        if sealevel_thrust < avaliable_thrust:
            throttle=1.
            partials['thottled_thrust', 'sealevel_thrust'] = 0
        elif (avaliable_thrust < 0) or (sealevel_thrust < 0):
            throttle=0.
            partials['thottled_thrust', 'sealevel_thrust'] = 0
        else:
            throttle=avaliable_thrust/sealevel_thrust
            partials['thottled_thrust', 'sealevel_thrust'] = (avaliable_thrust**2)*(-sealevel_thrust**(-2))

        partials['thottled_thrust', 'avaliable_thrust'] = throttle

