import numpy as np
from openmdao.api import ExplicitComponent


class PaybackperiodComp(ExplicitComponent):
def setup(self):
        #constant production plan in 10 years (1600)
        self.add_input('large_production_quentity')
        
        #constant learning curve effect 60%~95%
        self.add_input('learning_curve')
        
        #development etc.
        self.add_input('RDTE')
        
        #production cost per aircraft
        self.add_input('Flyaway')
        
        #constant flyhour per year (2500~4500)
        self.add_input('FH')
        
        #constant missions per year
        self.add_input('mission_year')
        
        # in dollar per mission
        self.add_input('Fuel')
        
        #maintenance per aircraft per year
        self.add_input('Main')
        
        self.add_input('passenger')
        self.add_input('ticket_price')
        
        self.add_output('Paybackperiod_year')
        
        self.declare_partials('Paybackperiod_year', 'RDTE')
        self.declare_partials('Paybackperiod_year', 'Flyaway')
        self.declare_partials('Paybackperiod_year', 'Fuel')
        self.declare_partials('Paybackperiod_year', 'Main')
        
 def compute(self, inputs, outputs):
  
        LQ = inputs['large_production_quentity']
        LC = inputs['learning_curve']
        RDTE = inputs['RDTE']
        Flyaway = inputs['Flyaway']
        FH = inputs['FH']
        MY = inputs['mission_year']
        Fuel = inputs['Fuel']
        Main = inputs['Main']
        Pass = inputs['passenger']
        Tic = inputs['ticket_price']
        
        

        outputs['Paybackperiod_year'] = ((Flyaway*LQ**np.log2(LC)+RDTE/LQ)*1.15*(1+0.9/20)+(MY*Fuel*(1+16/23)+Main)*1.011)/(Pass*Tic*MY)

def compute_partials(self, inputs, partials):
        LQ = inputs['large_production_quentity']
        LC = inputs['learning_curve']
        RDTE = inputs['RDTE']
        Flyaway = inputs['Flyaway']
        FH = inputs['FH']
        MY = inputs['mission_year']
        Fuel = inputs['Fuel']
        Main = inputs['Main']
        Pass = inputs['passenger']
        Tic = inputs['ticket_price']
        
        partials['Paybackperiod_year', 'RDTE']=1.20175*MY*Tic/Pass/LQ
        partials['Paybackperiod_year', 'Flyaway']=1.20175*MY*Tic*Q**(np.log(LC)/np.log(2))/Pass
        partials['Paybackperiod_year', 'Fuel']=1.7143*MY**2*Tic/Pass
        partials['Paybackperiod_year', 'Main']=1.011*MY*Tic/Pass
