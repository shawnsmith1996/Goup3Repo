from lsdo_viz.api import BaseViz, Frame

import seaborn as sns


sns.set()


class Viz(BaseViz):

    def setup(self):
        # self.use_latex_fonts()

        self.frame_name_format = 'output_{}'

        self.add_frame(Frame(
            height_in=8., width_in=12.,
            nrows=2, ncols=3,
            wspace=0.4, hspace=0.4,
        ), 1)

    def plot(self, data_dict_list, ind, video=False):
        x = data_dict_list[ind]['inputs_comp.x']
        h = data_dict_list[ind]['inputs_comp.h']

        self.get_frame(1).clear_all_axes()

        with self.get_frame(1)[0, 0] as ax:
            sns.lineplot(x=x, y=h, ax=ax)
            if video:
                ax.set_xlim(self.get_limits(
                    'inputs_comp.x', lower_margin=0.1, upper_margin=0.1,
                ))
                ax.set_ylim(self.get_limits(
                    'inputs_comp.h', lower_margin=0.1, upper_margin=0.1,
                ))
            ax.set_xlabel('x')
            ax.set_ylabel('h')

        with self.get_frame(1)[1, 0] as ax:
            sns.barplot(x=x, y=h, ax=ax)
            if video:
                ax.set_ylim(self.get_limits(
                    'inputs_comp.h', lower_margin=0.1, upper_margin=0.1,
                ))
            ax.set_xlabel('x')
            ax.set_ylabel('h')

            ax.get_xaxis().set_ticks([])

        with self.get_frame(1)[0, 1:] as ax:
            i_hist, h_hist = self.get_variable_history(data_dict_list, ind, 'compliance_comp.compliance', indices=0)

            p = sns.lineplot(x=i_hist, y=h_hist, ax=ax)
            # p.set(yscale='log')
            if video:
                ax.set_xlim((0, len(data_dict_list)))
                ax.set_ylim(self.get_limits(
                    'compliance_comp.compliance', lower_margin=0.1, upper_margin=0.1, mode='all',
                ))
            ax.set_ylabel('compliance')

        with self.get_frame(1)[1, 1:] as ax:
            i_hist, h_hist = self.get_variable_history(data_dict_list, ind, 'volume_comp.volume', indices=0)

            p = sns.lineplot(x=i_hist, y=h_hist, ax=ax)
            # p.set(yscale='log')
            if video:
                ax.set_xlim((0, len(data_dict_list)))
                ax.set_ylim(self.get_limits(
                    'volume_comp.volume', lower_margin=0.1, upper_margin=0.1, mode='all',
                ))
            ax.set_ylabel('volume')

        self.get_frame(1).write()