import numpy as np

from openmdao.api import ExplicitComponent


class RDTEComp(ExplicitComponent):

    #def initialize(self):
        #self.options.declare('Q', types=float)
        #self.options.declare('FTA', types=float)

    def setup(self):
        self.add_input('Q')
        self.add_input('FTA')
        # in lb
        self.add_input('We')
        self.add_input('velocity_ms')
        self.add_output('RDTE')

        self.declare_partials('RDTE', 'We')
        self.declare_partials('RDTE', 'velocity_ms')

    def compute(self, inputs, outputs):
        Q = inputs['Q']
        FTA = inputs['FTA']
        We = inputs['We']
        V = inputs['velocity_ms']

        outputs['RDTE'] = 2498*We**0.325*(V*1.94384)**0.282*FTA**1.21 + 91.3*We**0.63*(V*1.94384)**1.3 + 4.86*We**0.777*(V*1.94384)**0.894*Q**0.163*115 + 5.99*We**0.777*(V*1.94384)**0.696*Q**0.263*118

    def compute_partials(self, inputs, partials):
        Q = inputs['Q']
        FTA = inputs['FTA']

        We = inputs['We']
        V = inputs['velocity_ms']

        partials['RDTE', 'We'] = 811.85*FTA**1.21*(V*1.94384)**0.282/We**0.675+549.199*Q**0.263*(V*1.94384)**0.696/We**0.223+434.265*Q**0.163*(V*1.94384)**0.894/We**0.223+57.519*(V*1.94384)**1.3/We**0.37
        partials['RDTE', 'velocity_ms'] =  704.436*FTA**1.21*We**0.325/(V*1.94384)**0.718+491.947*Q**0.263*We**0.777/(V*1.94384)**0.304+499.657*Q**0.163*We**0.777/(V*1.94384)**0.106+118.69*(V*1.94384)**0.3*We**0.63
