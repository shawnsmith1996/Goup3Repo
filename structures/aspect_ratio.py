from openmdao.api import ExplicitComponent

class AspectRatio(ExplicitComponent):
    
    def setup(self):
        self.add_input('wing_span')
        self.add_input('chord')
        self.add_output('aspect_ratio')

        self.declare_partials('aspect_ratio', 'wing_span')
        self.declare_partials('aspect_ratio', 'chord')

    def compute(self, inputs, outputs):
        wing_span=inputs['wing_span']
        chord=inputs['chord']

        outputs['aspect_ratio'] = (wing_span / chord)

    def compute_partials(self, inputs, partials):

        wing_span=inputs['wing_span']
        chord=inputs['chord']

        partials['aspect_ratio', 'wing_span'] = 1 / chord
        partials['aspect_ratio', 'chord'] = -wing_span / (chord**2)