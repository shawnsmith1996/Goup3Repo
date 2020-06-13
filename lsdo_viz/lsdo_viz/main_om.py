import sys
import argparse

from lsdo_viz.problem import Problem
from lsdo_viz.utils import exec_python_file, get_viz, get_args, clean


def main_om(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument('args_file_name', nargs='?', default='viz_args.py')
    parser.add_argument('--run', '-r', nargs='?', default=None, const=True)
    parser.add_argument('--optimize', '-o', nargs='?', default=None, const=True)
    parser.add_argument('--clean_data', '-cd', nargs='?', default=None, const=True)
    parser.add_argument('--clean_frames', '-cf', nargs='?', default=None, const=True)
    parsed_args = parser.parse_args(args)

    args = get_args(parsed_args.args_file_name)

    if parsed_args.clean_data:
        clean(args.data_dir)

    if parsed_args.clean_frames:
        clean(args.frames_dir)

    modes = []
    if parsed_args.run:
        modes.append('run_model')
    if parsed_args.optimize:
        modes.append('run_driver')

    Problem.args = args
    Problem.viz = get_viz(args.viz_file_name)

    for mode in modes:
        Problem.mode = mode

        exec_python_file(args.run_file_name)