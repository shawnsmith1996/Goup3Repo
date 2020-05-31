#!/usr/bin/env python
# coding: utf-8

# In[1]:


from openmdao.api import ExplicitComponent
import numpy as np

class Avaliable_Thrust(ExplicitComponent):

        
    def setup(self):
        self.add_input('sealevel_thrust')
        self.add_input('density')
        self.add_input('sealevel_density')
        self.add_output('avaliable_thrust')
        
        self.declare_partials('avaliable_thrust', 'sealevel_thrust')
        self.declare_partials('avaliable_thrust', 'density')
        self.declare_partials('avaliable_thrust', 'sealevel_density')

    def compute(self, inputs, outputs):
        sealv_thrust=inputs['sealevel_thrust']
        dens=inputs['density']
        sealv_dens=inputs['sealevel_density']
        outputs['avaliable_thrust'] = (sealv_thrust * dens) / (sealv_dens)
        
#         comp = PowerCombinationComp(
#            shape=shape,
#            out_name='available_thrust',
#            powers_dict=dict(
#                mach_number=0.,
#                sealevel_thrust=1.,
#                density=1.,
#                sealevel_density=-1.,
#            )
#        )

    def compute_partials(self, inputs, partials):

        sealv_thrust=inputs['sealevel_thrust']
        dens=inputs['density']
        sealv_dens=inputs['sealevel_density']

        partials['avaliable_thrust', 'sealevel_thrust'] =(dens) / (sealv_dens)
        
        partials['avaliable_thrust', 'density'] =(sealv_thrust) / (sealv_dens)
        
        partials['avaliable_thrust', 'sealevel_density'] =(-1*sealv_thrust * dens) / (sealv_dens**2)


# In[ ]:




