#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

from openmdao.api import ExplicitComponent


class Thottled_Thrust(ExplicitComponent):


    def setup(self):
        self.add_input('sealevel_thrust')
        self.add_input('avaliable_thrust')
        self.add_output('thottled_thrust')

        self.declare_partials('thottled_thrust', 'sealevel_thrust')
        self.declare_partials('thottled_thrust', 'avaliable_thrust')

    def compute(self, inputs, outputs):
        sealevel_thrust=inputs['sealevel_thrust']
        avaliable_thrust=inputs['avaliable_thrust']
        if 0.5*sealevel_thrust > avaliable_thrust:
            throttle=1.
        elif avaliable_thrust < 0 or sealevel_thrust < 0:
            throttle=0.
        else:
            throttle=0.5*(sealevel_thrust)/(avaliable_thrust)

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
# thottled_thrust = 0.5*(sealevel_thrust)
# if 0.5*sealevel_thrust > avaliable_thrust:
# thottled_thrust = avaliable_thrust
# if 0(avaliable_thrust < 0) or (sealevel_thrust < 0):
# thottled_thrust = 0
        sealevel_thrust=inputs['sealevel_thrust']
        avaliable_thrust=inputs['avaliable_thrust']
        if 0.5*sealevel_thrust > avaliable_thrust:
            throttle=1.
            partials['thottled_thrust', 'sealevel_thrust'] = 0
            partials['thottled_thrust', 'avaliable_thrust'] = 1
        elif (avaliable_thrust < 0) or (sealevel_thrust < 0):
            throttle=0.
            partials['thottled_thrust', 'sealevel_thrust'] = 0
            partials['thottled_thrust', 'avaliable_thrust'] = 0
        else:
            throttle=0.5*(sealevel_thrust)/(avaliable_thrust)
            partials['thottled_thrust', 'sealevel_thrust'] = 0.5
            partials['thottled_thrust', 'avaliable_thrust'] = 0

