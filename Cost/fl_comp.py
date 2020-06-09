from openmdao.api import ExplicitComponent


class FlyawayComp(ExplicitComponent):

    #def initialize(self):
        #self.options.declare('Q', types=float)
        #self.options.declare('Tinlet', types=float)
        #self.options.declare('EN', types=float)
        #self.options.declare('sealevel_thrust', types=float)
        #self.options.declare('M_max', types=float)


    def setup(self):
        self.add_input('We')
        self.add_input('speed')

        self.add_input('Q')
        self.add_input('Tinlet')
        self.add_input('EN')
        self.add_input('M_max')
        self.add_input('T_max')

        self.add_output('Flyaway')

        self.declare_partials('Flyaway', 'We')
        self.declare_partials('Flyaway', 'speed')
        

    def compute(self, inputs, outputs):
        #Q = self.options['Q']
        #Tinlet = self.options['Tinlet']
        #EN = self.options['EN']
        #Tmax = self.options['T_max']
        #Mmax = self.options['M_max']
        EN=inputs['EN']
        Tinlet=inputs['Tinlet']
        Q = inputs['Q']
        We = inputs['We']
        V = inputs['speed']
        Tmax = inputs['T_max']
        Mmax = inputs['M_max']

        outputs['Flyaway'] = 1.25*(7.37*We**0.82*(V*1.94384)**0.484*Q**0.641*108/Q+0.133*7.37*We**0.82*(V*1.94384)**0.484*Q**0.641*98/Q+3112*(0.043*Tmax+243.25*Mmax+0.969*Tinlet-2228)*EN+22.1*We**0.921*(V*1.94384)**0.621*Q**0.799/Q)

    def compute_partials(self, inputs, partials):
        #Q = self.options['Q']
        #Tinlet = self.options['Tinlet']
        #EN = self.options['EN']
        #Tmax = self.options['T_max']
        #Mmax = self.options['M_max']
        #EN=inputs['EN']
        #Tinlet=inputs['Tinlet']
        Q = inputs['Q']
        We = inputs['We']
        V = inputs['speed']
        #Tmax = inputs['T_max']
        #Mmax = inputs['M_max']
        

        partials['Flyaway', 'We'] =25.4426*Q**0.799/Q*(V*1.94384)**0.621/We**0.079+914.321*Q**0.641/Q*(V*1.94384)**0.484/We**0.18 
        partials['Flyaway', 'speed'] = 17.1551*Q**0.799/Q*We**0.921/(V*1.94384)**0.379+539.672*Q**0.641/Q*We**0.82/(V*1.94384)**0.516
