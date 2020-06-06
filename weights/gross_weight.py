from openmdao.api import ExplicitComponent

class GrossWeight(ExplicitComponent):

    def setup(self):
        self.add_input('payload_weight')
        self.add_input('crew_weight')
        self.add_input('empty_weight_fraction')
        self.add_input('Wfr')
        self.add_output('gross_weight')

        self.declare_partials('gross_weight', 'payload_weight')
        self.declare_partials('gross_weight', 'crew_weight')
        self.declare_partials('gross_weight', 'empty_weight_fraction')
        self.declare_partials('gross_weight', 'Wfr')

    def compute(self, inputs, outputs):
        Wp=inputs['payload_weight']
        Wc=inputs['crew_weight']
        Weo=inputs['empty_weight_fraction']
        Wfo=inputs['Wfr']

        outputs['gross_weight'] = (Wp + Wc) / (1 - Weo - Wfo)

    def compute_partials(self, inputs, partials):
        Wp=inputs['payload_weight']
        Wc=inputs['crew_weight']
        Weo=inputs['empty_weight_fraction']
        Wfo=inputs['Wfr']

        partials['gross_weight', 'payload_weight'] = 1 / (1 - Weo - Wfo)
        partials['gross_weight', 'crew_weight'] = 1 / (1 - Weo - Wfo)
        partials['gross_weight', 'empty_weight_fraction'] = (Wp + Wc)/((1 - Weo - Wfo)**2)
        partials['gross_weight', 'Wfr'] = (Wp + Wc)/((1 - Weo - Wfo)**2)