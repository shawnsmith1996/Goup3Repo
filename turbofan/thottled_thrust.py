#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np

from openmdao.api import ExplicitComponent


class Thottled_Thrust(ExplicitComponent):


    def setup(self):
        self.add_input('drag')
        self.add_input('avaliable_thrust')
        self.add_output('thottled_thrust')

        self.declare_partials('thottled_thrust', 'drag')
        self.declare_partials('thottled_thrust', 'avaliable_thrust')

    def compute(self, inputs, outputs):
        drag=inputs['drag']
        avaliable_thrust=inputs['avaliable_thrust']
        if drag > avaliable_thrust:
            throttle=1.
        elif avaliable_thrust < 0 or drag < 0:
            throttle=0.
        else:
            throttle=(drag)/(avaliable_thrust)

        outputs['thottled_thrust'] = (throttle * avaliable_thrust)

    def compute_partials(self, inputs, partials):

        drag=inputs['drag']
        avaliable_thrust=inputs['avaliable_thrust']
        if drag > avaliable_thrust:
            throttle=1.
            partials['thottled_thrust', 'drag'] = 0
            partials['thottled_thrust', 'avaliable_thrust'] = 1
        elif (avaliable_thrust < 0) or (drag < 0):
            throttle=0.
            partials['thottled_thrust', 'drag'] = 0
            partials['thottled_thrust', 'avaliable_thrust'] = 0
        else:
            throttle=(drag)/(avaliable_thrust)
            partials['thottled_thrust', 'drag'] = 1
            partials['thottled_thrust', 'avaliable_thrust'] = 0

