import os
import sys
import glob
import argparse

from lsdo_viz.problem import Problem
from lsdo_viz.utils import clean, get_viz, get_args, exec_python_file


def main_viz(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('args_file_name', nargs='?', default='viz_args.py')
    parser.add_argument('--clean_data', '-cd', nargs='?', default=None, const=True)
    parser.add_argument('--clean_frames', '-cf', nargs='?', default=None, const=True)
    parser.add_argument('--viz_initial', '-vi', nargs='?', default=None, const=True)
    parser.add_argument('--viz_final', '-vf', nargs='?', default=None, const=True)
    parser.add_argument('--viz_initial_show', '-vis', nargs='?', default=None, const=True)
    parser.add_argument('--viz_final_show', '-vfs', nargs='?', default=None, const=True)
    parser.add_argument('--viz_all', '-va', nargs='?', default=None, const=True)
    parser.add_argument('--movie', '-m', nargs='?', default=None, const=True)
    parsed_args = parser.parse_args(args)

    args = get_args(parsed_args.args_file_name)

    show = parsed_args.viz_initial_show or parsed_args.viz_final_show

    if not show:
        import matplotlib
        matplotlib.use('Agg')

    if parsed_args.clean_data:
        clean(args.data_dir)

    if parsed_args.clean_frames:
        clean(args.frames_dir)

    modes = []
    if parsed_args.viz_initial or parsed_args.viz_initial_show:
        modes.append('viz_initial')
    if parsed_args.viz_final or parsed_args.viz_final_show:
        modes.append('viz_final')
    if parsed_args.viz_all:
        modes.append('viz_all')
    if parsed_args.movie:
        modes.append('movie')

    Problem.args = args
    Problem.viz = get_viz(args.viz_file_name)
    Problem.viz.args = args
    Problem.viz.show = show

    for mode in modes:
        Problem.mode = mode

        exec_python_file(args.run_file_name)