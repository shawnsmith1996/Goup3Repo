import numpy as np
import math

from openmdao.api import ExplicitComponent

class Range(ExplicitComponent):

    def setup(self):
        self.add_input('specific_fuel_cosum')
        self.add_input('LD')
        self.add_input('velocity_ms')
        self.add_input('operating_empty_weight')
        #self.add_inputs('payload_weight')
        self.add_input('fuel_weight_ratio')
        self.add_input('gross_weight')
        self.add_input('MTOW')
        self.add_output('range')

        self.declare_partials('range', 'specific_fuel_consum')
        self.declare_partials('range', 'LD')
        self.declare_partials('range', 'velocity_ms')

    def compute(self, inputs, outputs):
        SFC = inputs['specific_fuel_consum']
        LD = inputs['LD']
        V = inputs['velocity_ms']
        #Woe = inputs['operating_empty_weight']
    
        Wto = inputs['MTOW']
        Wo = inputs['gross_weight']
        Wfr = inputs['fuel_weight_ratio']

        Wf = Wfr *Wo
        #Woe = Wo - Wpl + Wf
        #Wto = Woe + Wpl + Wf
        g = 9.81
        Mff = 1 - Wf/Wto
        W45 = 0.99 *0.99 *0.995 *0.98 *0.99 *0.992 *(1/Mff)

        outputs['range'] = (1/1000)*(V / (g*SFC) *(LD) *math.log10(W45))

    def compute_partials(self, inputs, partials):
        SFC = inputs['specific_fuel_consum']
        LD = inputs['LD']
        V = inputs['velocity_ms']
        #Woe = inputs['operating_empty_weight']
        Wto = inputs['MTOW']
        Wf = inputs['fuel_weight']
            
        g = 9.81
        Mff = 1 - Wf/Wto
        W45 = 0.99 *0.99 *0.995 *0.98 *0.99 *0.992 *(1/Mff)

        partials['range', 'specific_fuel_consum'] = -(1/1000)*(V / (g*(SFC **2)) *(LD) *math.log10(W45))
        partials['range', 'LD'] = (1/1000)*(V / (g*SFC) *math.log10(W45))
        partials['range', 'velocity_ms'] = (1/1000)*(1 / (g*SFC) *(LD) *math.log10(W45))