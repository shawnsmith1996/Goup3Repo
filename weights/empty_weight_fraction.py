from openmdao.api import ExplicitComponent

class EmptyWeightFraction(ExplicitComponent):

    def setup(self):
        self.add_input('MTOW')
        self.add_output('empty_weight_fraction')

        self.declare_partials('empty_weight_fraction', 'MTOW')

    def compute(self, inputs, outputs):
        MTOW=inputs['MTOW']
        
        outputs['empty_weight_fraction'] = 0.97 *MTOW **-0.06

    def compute_partials(self, inputs, partials):
        MTOW=inputs['MTOW']

        partials['empty_weight_fraction', 'MTOW'] = -0.0582 *MTOW **-1.06