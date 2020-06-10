import numpy as np  
from openmdao.api import ExplicitComponent


class FuelWeightRatio(ExplicitComponent):




    def setup(self):
        self.add_input('R')
        self.add_input('specific_fuel_consum')
        self.add_input('lift_to_drag_ratio')
        self.add_input('speed')


        self.add_output('Wfr')

        self.declare_partials('Wfr', 'speed')
        self.declare_partials('Wfr', 'lift_to_drag_ratio')
        self.declare_partials('Wfr', 'specific_fuel_consum')

    def compute(self, inputs, outputs):
  
        R=inputs['R']
        SFC = inputs['specific_fuel_consum']
        LD = inputs['lift_to_drag_ratio']
        V = inputs['speed']
     

        outputs['Wfr'] = 1-np.exp(-(9.807*R*SFC/(V*LD)))
        
    def compute_partials(self, inputs, partials):
   
        R=inputs['R']
        SFC = inputs['specific_fuel_consum']
        LD = inputs['lift_to_drag_ratio']
        V = inputs['speed']
        

        partials['Wfr', 'speed'] = ((-9.807/LD)*R*(SFC/V**2))*np.exp(-9.807/LD*R*SFC/V)
        partials['Wfr', 'lift_to_drag_ratio'] = ((-9.807*R*SFC/LD**2)/V)*np.exp(-9.807/LD*R*SFC/V)
        partials['Wfr', 'specific_fuel_consum'] =-((-9.807/LD)*R/V)*np.exp(-9.807/LD*R*SFC/V)
