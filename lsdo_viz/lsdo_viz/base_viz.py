import numpy as np
import os
from collections import Iterable

from lsdo_viz.utils import get_numbered_file_name_general, get_new_file_path
from lsdo_viz.movie_utils import make_mov


class BaseViz(object):

    def __init__(self):
        self.args = None
        self.show = False
        self.virtual_mode = False
        self.prob = None
        self.var_ranges = dict(
            last=dict(),
            all=dict(),
        )

        self.frames = dict()
        self.frame_name_format = 'output'

    def _make_movies(self):
        for frame_name in self.frames:
            frame = self.frames[frame_name]

            for ext_name in ['mov', 'avi']:
                try:
                    os.remove('{}.{}'.format(frame.frame_name, ext_name))
                except:
                    pass
            make_mov(
                get_numbered_file_name_general(
                    '{}/{}'.format(self.args.frames_dir, frame.frame_name),
                    frame.ext_name,
                ),
                self.args.fps,
                frame.frame_name,
            )

    def _compute_limits(self, data_dict_list, var_names):
        for mode in ['last', 'all']:
            for var_name in var_names:
                min_ = np.inf
                max_ = -np.inf

                if mode == 'all':
                    indices = range(len(data_dict_list))
                elif mode == 'last':
                    indices = [len(data_dict_list) - 1]

                for ind in indices:
                    data_dict = data_dict_list[ind]

                    array = data_dict[var_name]

                    min_ = min(
                        min_,
                        np.min(array),
                    )

                    max_ = max(
                        max_,
                        np.max(array),
                    )

                self.var_ranges[mode][var_name] = (min_, max_)

    def get_limits(
        self, var_name, 
        lower_margin=0.1, upper_margin=0.1, 
        mode='last', scaler=1.,
    ):
        min_, max_ = self.var_ranges[mode][var_name]

        range_ = max_ - min_

        return (
            scaler * (min_ - range_ * lower_margin),
            scaler * (max_ + range_ * upper_margin),
        )

    def get_variable_history(self, data_dict_list, current_ind, var_name, indices=None):
        if indices is None:
            indices = 0

        if current_ind < 0:
            current_ind += len(data_dict_list)

        history = []
        for ind in range(current_ind + 1):
            history.append(data_dict_list[ind][var_name][indices])

        return np.arange(len(history)), history

    def use_latex_fonts(self):
        from matplotlib import rc
        rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
        rc('text', usetex=True)

    def add_frame(self, frame, frame_name_args=None):
        if not isinstance(frame_name_args, Iterable):
            frame_name_args = (frame_name_args,)

        frame_name = self.frame_name_format.format(*frame_name_args)
        self.frames[frame_name] = frame

        frame.frame_name = frame_name
        frame.viz = self

    def get_frame(self, frame_name_args=None):
        if not isinstance(frame_name_args, Iterable):
            frame_name_args = (frame_name_args,)

        frame_name = self.frame_name_format.format(*frame_name_args)
        return self.frames[frame_name]

    def get_frame_path(self, frame_name, ext_name):
        frame_path = get_new_file_path(
            self.args.frames_dir,
            frame_name, 
            ext_name,
        )[1]

        return frame_path

    def plot(self, data_dict_list, ind, viz_type, video=False):
        pass

    def setup(self):
        pass