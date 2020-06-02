#!/usr/bin/env python
# coding: utf-8

# In[1]:


from openmdao.api import ExplicitComponent
import numpy as np

class Zerospeed_Thrust(ExplicitComponent):

        
    def setup(self):
        self.add_input('sealevel_thrust')
        self.add_input('density')

        self.add_output('zerospeed_thrust')
        
        self.declare_partials('zerospeed_thrust', 'sealevel_thrust')
        self.declare_partials('zerospeed_thrust', 'density')
#        self.declare_partials('zerospeed_thrust', 'sealevel_density')

    def compute(self, inputs, outputs):
        sealv_thrust=inputs['sealevel_thrust']
        dens=inputs['density']
        sealv_dens=1.225
        outputs['zerospeed_thrust'] = (sealv_thrust * dens) / (sealv_dens)
        
#         comp = PowerCombinationComp(
#            shape=shape,
#            out_name='zerospeed_thrust',
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
        sealv_dens=1.225

        partials['zerospeed_thrust', 'sealevel_thrust'] =(dens) / (sealv_dens)
        
        partials['zerospeed_thrust', 'density'] =(sealv_thrust) / (sealv_dens)
        
#        partials['avaliable_thrust', 'sealevel_density'] =(-1*sealv_thrust * dens) / (sealv_dens**2)


# In[ ]:




