#!/usr/bin/env python
# coding: utf-8

# In[1]:


from openmdao.api import ExplicitComponent

class TurbofanGroup(ExplicitComponent):

    def initialize(self):
        self.promotes = ['sealevel_thrust']
        
    def setup(self):
        self.add_input('alpha')
        self.add_input('CLa')
        self.add_input('CL0')
        self.add_output('CL')
        
        self.declare_partials('CL', 'alpha')
        self.declare_partials('CL', 'CLa')
        self.declare_partials('CL', 'CL0', val=1.)
        
        
        self.add_input('mach_number')
        self.add_input('sealevel_thrust')
        self.add_input('density')
        self.add_input('sealevel_density')
        self.add_input('throttle')
        
        self.add_output('avaliable_thrust')
        self.add_output('thrust')
        self.add_output('mass_flow_rate')
        

    def Avaliable_Thrust(self, inputs, outputs):
        mach_n=inputs['mach_number']
        sealv_thrust=inputs['sealevel_thrust']
        dens=inputs['density']
        sealv_dens=inputs['sealevel_density']
        
        outputs['avaliable_thrust'] = (sealv_thrust * dens) / (sealv_dens)
        
 #        comp = PowerCombinationComp(
  #          shape=shape,
   #         out_name='available_thrust',
    #        powers_dict=dict(
     #           mach_number=0.,
      #          sealevel_thrust=1.,
       #         density=1.,
        #        sealevel_density=-1.,
        #    ),
        #)
    def Thrust(self, inputs, outputs):
        throttle=inputs['throttle']
        a_thrust=inputs['sealevel_thrust']

        
        outputs['thrust'] = (throttle * a_thrust)
    
    
#    def Thrust(self, inputs, outputs):
 #       comp = PowerCombinationComp(
  #          shape=shape,
   #         out_name='thrust',
    #        powers_dict=dict(
     #           throttle=1.,
      #          available_thrust=1.,
       #     ),
        #)
    def Mass_Flow_Rate(self, inputs, outputs):
        throttle=inputs['thrust']
        a_thrust=inputs['mass_flow_rate_coeffecient']

        
        outputs['thrust'] = (throttle * a_thrust)
        
#    def Mass_Flow_Rate(self, inputs, outputs):
 #       comp = PowerCombinationComp(
  #          shape=shape,
   #         out_name='mass_flow_rate',
    #        coeff=module['thrust_specific_fuel_consumption'],
     #       powers_dict=dict(
      #          thrust=1.,
       #     ),
        #)


    def Coeffecient_of_Lift(self, inputs, outputs):
        alpha = inputs['alpha']
        CLa = inputs['CLa']
        CL0 = inputs['CL0']

        outputs['CL'] = CLa * alpha + CL0

    def Partial_Coeffecient(self, inputs, partials):
        alpha = inputs['alpha']
        CLa = inputs['CLa']
        CL0 = inputs['CL0']

        partials['CL', 'alpha'] = CLa
        partials['CL', 'CLa'] = alpha
        
       


# In[ ]:




