from openmdao.api import ExplicitComponent


class Fuel_Burn(ExplicitComponent):


    def setup(self):
        self.add_input('specific_fuel_consum')
        self.add_input('thottled_thrust')
        self.add_output('fuel_burn')

        self.declare_partials('fuel_burn', 'thottled_thrust')
        self.declare_partials('fuel_burn', 'specific_fuel_consum')

    def compute(self, inputs, outputs):
        thrust=inputs['thottled_thrust']
        specific_fuel_consum=inputs['specific_fuel_consum']

        outputs['fuel_burn'] = (thrust * specific_fuel_consum)
    
    
#    def Thrust(self, inputs, outputs):
#        comp = PowerCombinationComp(
#            shape=shape,
#            out_name='thrust',
#            powers_dict=dict(
#                thrust_ratio=1.,
#                zero_spd_thrust=1.,
#            ),
#        )

    def compute_partials(self, inputs, partials):

        thrust=inputs['thottled_thrust']
        specific_fuel_consum=inputs['specific_fuel_consum']

        partials['fuel_burn', 'thottled_thrust'] = specific_fuel_consum
        partials['fuel_burn', 'specific_fuel_consum'] = thrust

