import numpy as np
import types

from openmdao.api import Problem as OMProblem
from openmdao.api import AnalysisError

from lsdo_viz.writer import Writer
from lsdo_viz.print_opt_variables import print_opt_variables
from lsdo_viz.utils import make_dir, get_args, clean, VirtualDict, get_numbered_file_name_general


def new_solve_nonlinear(self):
    if self.problem.args.print_nonlinear_status:
        print('Executing run_model...')
    result = self._solve_nonlinear_original()
    if self.problem.args.print_nonlinear_status:
        print('Finished run_model.')

    self.writer.write()

    if self.problem.args.print_opt_variables:
        print_opt_variables(self.problem, print_mean=True)

    if np.any(np.isnan(self._outputs._data)) or np.any(np.isinf(self._outputs._data)):
        print('*' * 30)
        print('NaN detected')
        print('*' * 30)
        raise AnalysisError()

    return result

def new_solve_linear(self, *args, **kwargs):
    if self.problem.args.print_linear_status:
        print('Executing solve_linear...')
    result = self._solve_linear_original(*args, **kwargs)
    if self.problem.args.print_linear_status:
        print('Finished solve_linear.')

    return result


class Problem(OMProblem):

    mode = ''

    args = None
    viz = None

    def __init__(self, *args, **kwargs):
        super(Problem, self).__init__(*args, **kwargs)

        self.writer = None

    def run(self):
        mode = self.mode

        if mode == 'run_model':
            self.run_model()
        elif mode == 'run_driver':
            self.run_driver()
        elif 'viz' in mode:
            data_dict_list = self.writer.read()

            make_dir(self.args.frames_dir)

            if mode == 'viz_initial':
                viz_indices = [0]
                video = False
            elif mode == 'viz_final':
                viz_indices = [-1]
                video = False
            elif mode == 'viz_all':
                viz_indices = range(0, len(data_dict_list), self.args.stride)
                video = True

                clean(self.args.frames_dir)

            self.run_visualization(data_dict_list, viz_indices, video)

            if mode == 'viz_all':
                self.viz._make_movies()
        elif mode == 'movie':
            self.viz._make_movies()

    def setup(self, *args, **kwargs):
        super(Problem, self).setup(*args, **kwargs)

        self.final_setup()

        if self.viz:
            model = self.model

            model._solve_nonlinear_original = model._solve_nonlinear
            model._solve_nonlinear = types.MethodType(new_solve_nonlinear, model)
            model._solve_linear_original = model._solve_linear
            model._solve_linear = types.MethodType(new_solve_linear, model)
            model.problem = self

            virtual_dict = VirtualDict()
            self.viz.prob = self
            self.viz.setup()
            self.viz.virtual_mode = True
            self.viz.plot([virtual_dict], 0, False)
            self.var_names = virtual_dict.var_names

            self.writer = model.writer = Writer(
                data_dir=self.args.data_dir,
                data_file_name=self.args.data_file_name,
                system=model,
                var_names=virtual_dict.var_names,
            )

    def run_driver(self):
        if self.writer:
            self.writer.clean()
        super(Problem, self).run_driver()

    def run_visualization(self, data_dict_list, viz_indices, video):
        import matplotlib.pyplot as plt

        for ind in viz_indices:
            print('Plotting data set index: ', ind)

            self.viz._compute_limits(data_dict_list, self.var_names)
            self.viz.virtual_mode = False
            self.viz.plot(data_dict_list, ind, video=video)
            if self.viz.show:
                plt.show()