import numpy as np
from openmdao.api import Group, ExplicitComponent
from lsdo_utils.api import OptionsDictionary, LinearPowerCombinationComp,LinearCombinationComp, PowerCombinationComp, GeneralOperationComp, ElementwiseMinComp


from aerodynamics.pressure_comp import PressureComp
from aerodynamics.temperature_comp import TemperatureComp
from aerodynamics.density_comp import DensityComp

from aerodynamics.wave_drag_coeff_comp import WaveDragCoeffComp
class AeroGroup(Group):
    def initialize(self):
        self.options.declare('shape', types=tuple)

    def setup(self):
        shape = self.options['shape']

        comp = PressureComp()
        self.add_subsystem('pressure_comp', comp, promotes=['*'])

        comp = TemperatureComp()
        self.add_subsystem('temperature_comp', comp, promotes=['*'])

        comp = DensityComp() 
        self.add_subsystem('density_comp', comp, promotes=['*'])

        R=287.058
        gamma=1.4
        comp = PowerCombinationComp(#
            shape=shape,
            coeff=1/np.sqrt(gamma*R),
            out_name='M_inf',
            powers_dict=dict(
                velocity_ms=1.,
                temperature=-0.5,
            )
        )
        self.add_subsystem('mach_comp', comp, promotes=['*'])


## Need CDv CD0 CL0 CLa 

        comp = LinearPowerCombinationComp(
            shape=shape,
            out_name='CL',
            terms_list=[
                (1.,dict(
                alpha=1.,
                CLa=1.,
                )),
                (1.,dict(
                CL0=1.,
                )),
            ],
        )
        self.add_subsystem('CL_comp', comp, promotes=['*'])

        comp=WaveDragCoeffComp()
        self.add_subsystem('CDw_comp', comp, promotes=['*'])

        e=0.7
        comp = PowerCombinationComp(
            shape=shape,
            coeff=1/(np.pi*e),
            out_name='CDi',
            powers_dict=dict(
                CL=2.,
                aspect_ratio=-1,
            )
        )
        self.add_subsystem('CDi_comp', comp, promotes=['*'])

        comp = LinearCombinationComp(
            shape=shape,
            in_names=['CDi','CDv','CDw','CD0'],
            out_name='CD',
            coeffs=[1.,1.,1.,1.],
        )
        self.add_subsystem('CD_comp', comp, promotes=['*'])      

        comp = PowerCombinationComp(
            shape=shape,
            coeff=1/2,
            out_name='drag',
            powers_dict=dict(
                velocity_ms=2.,
                density=1,
                CD = 1.,
            )
        )
        self.add_subsystem('drag_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='LD',#lift over drag
            powers_dict=dict(
                CL = 1.,
                CD = -1.,
            )
        )
        self.add_subsystem('lift_over_drag_comp', comp, promotes=['*'])

        comp = PowerCombinationComp(
            shape=shape,
            out_name='Lift',
            powers_dict=dict(
                D = 1.,
                LD = 1
            )
        )
        self.add_subsystem('lift_comp', comp, promotes=['*'])
