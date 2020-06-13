import matplotlib.pyplot as plt
from contextlib import contextmanager
import traceback

from lsdo_viz.utils import get_new_file_path


class Frame(object):

    def __init__(
        self,
        width_in=5., height_in=5., 
        nrows=1, ncols=1,
        wspace=0.2, hspace=0.2,
        **kwargs,
    ):
        self.viz = None
        self.frame_name = None
        self.ext_name = 'png'

        self.fig = plt.figure(figsize=(width_in, height_in))

        self.gs = self.fig.add_gridspec(
            nrows=nrows, ncols=ncols,
            wspace=wspace, hspace=hspace,
        )

        self.axes = dict()

    @contextmanager
    def __getitem__(self, gs_key):
        key0 = gs_key[0]
        key1 = gs_key[1]

        if isinstance(key0, slice):
            key0 = (key0.start, key0.stop, key0.step)
        if isinstance(key1, slice):
            key1 = (key1.start, key1.stop, key1.step)

        key = (key0, key1)

        if key not in self.axes:
            self.axes[key] = self.fig.add_subplot(self.gs[gs_key])

        try:
            yield self.axes[key]
        except Exception as e:
            if not self.viz.virtual_mode:
                print(traceback.format_exc())

    def clear_all_axes(self):
        for key in self.axes:
            self.axes[key].clear()

    def write(self):
        if not self.viz.virtual_mode:
            frame_path = get_new_file_path(
                self.viz.args.frames_dir,
                self.frame_name, 
                self.ext_name
            )[1]
            self.fig.savefig(frame_path, dpi=self.viz.args.savefig_dpi)