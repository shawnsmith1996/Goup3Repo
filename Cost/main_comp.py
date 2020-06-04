from openmdao.api import ExplicitComponent


class MainComp(ExplicitComponent):

    #def initialize(self):
        #self.options.declare('MHFH', types=float)
        #self.options.declare('FH', types=float)
        #self.options.declare('EN', types=float)
        #elf.options.declare('Tinlet', types=float)
        #elf.options.declare('T_max', types=float)
        #self.options.declare('M_max', types=float)
#        3*Tmax + 243.25*Mmax + 0.969*Tinlet- 2228)/10**6 + 14.2 + (58*3112*(0.043*T+ 243.25*M + 0.969*H- 2228)/10**6 - 26.1)
    def setup(self):
        self.add_input('Flyaway')
        self.add_input('MHFH')
        self.add_input('FH')
        self.add_input('EN')
        self.add_input('Tinlet')
        self.add_input('T_max')
        self.add_input('M_max')

        
        self.add_output('Main')

        self.declare_partials('Main', 'Flyaway')

    def compute(self, inputs, outputs):
        Flyaway = inputs['Flyaway']
        MHFH= inputs['MHFH']
        FH= inputs['FH']
        Tinlet= inputs['Tinlet']
        Tmax= inputs['T_max']
        Mmax= inputs['M_max']
        EN= inputs['EN']

        outputs['Main'] = MHFH*FH*108+(3.3*(Flyaway-3112*(0.043*Tmax + 243.25*Mmax + 0.969*Tinlet- 2228)/10**6 + 14.2 + (58*3112*(0.043*Tmax + 243.25*Mmax + 0.969*Tinlet- 2228))/10**6 - 26.1)*EN)*FH

    def compute_partials(self, inputs, partials):
        We = inputs['Flyaway']
        Tinlet= inputs['Tinlet']
        EN= inputs['EN']
        

        partials['Main', 'Flyaway'] = 3.3*Tinlet*EN

