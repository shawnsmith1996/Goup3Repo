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
        throttle=(drag)/(avaliable_thrust) 

        outputs['thottled_thrust'] = (throttle * avaliable_thrust)

    def compute_partials(self, inputs, partials):
        partials['thottled_thrust', 'drag'] = 1
        partials['thottled_thrust', 'avaliable_thrust'] = 0

