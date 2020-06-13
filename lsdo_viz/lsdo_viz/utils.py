import os
import sys
import glob
import importlib
import traceback
import lsdo_viz.default_viz_args as default_viz_args


working_dir_path = os.getcwd()
working_dir_path = working_dir_path.replace(r'\\ ', r'\ ')
working_dir_path = working_dir_path.replace(r'\ ', r' ')


def suppress_plot_show():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    return plt


def use_latex_fonts():
    from matplotlib import rc
    rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    rc('text', usetex=True)


def get_cwd():
    return working_dir_path


def make_dir(dir_name):
    data_dir_path = r'{}/{}'.format(working_dir_path, dir_name)
    if not os.path.isdir(data_dir_path):
        os.mkdir(data_dir_path)


def get_viz(viz_file_name):
    try:
        viz_file_path = r'{}/{}'.format(working_dir_path, viz_file_name)
        spec = importlib.util.spec_from_file_location('viz', viz_file_path)
        viz = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(viz)
        return viz.Viz()
    except:
        print(traceback.format_exc())
    return None


def get_args(args_file_name):
    try:
        args_file_path = r'{}/{}'.format(working_dir_path, args_file_name)
        spec = importlib.util.spec_from_file_location('viz_args', args_file_path)
        viz_args = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(viz_args)
        return viz_args
    except:
        return default_viz_args


def get_numbered_file_name(file_name, ind, ext_name):
    return r'{0}.{1:05d}.{2}'.format(
        file_name, 
        ind,
        ext_name,
    )


def get_numbered_file_name_general(file_name, ext_name):
    return r'{0}.%05d.{1}'.format(
        file_name,
        ext_name,
    )


def get_new_file_path(dir_name, file_name, ext_name):
    ind = 0
    while True:
        rel_file_path = r'{}/{}'.format(
            dir_name, 
            get_numbered_file_name(
                file_name, 
                ind,
                ext_name,
            ),
        )
        abs_file_path = r'{}/{}'.format(
            working_dir_path, 
            rel_file_path,
        )

        if not os.path.isfile(abs_file_path):
            break

        ind += 1
    
    return abs_file_path, rel_file_path


def clean(dir_name):
    file_paths = glob.glob(r'{}/{}/*'.format(working_dir_path, dir_name))
    for file_path in file_paths:
        try:
            os.remove(file_path)
        except:
            pass


def exec_python_file(run_file_name):
    sys.path.insert(0, os.path.dirname(run_file_name))

    with open(run_file_name, 'rb') as fp:
        lines = fp.read().split(b'\n')
        code = compile(b'\n'.join(lines), run_file_name, 'exec')

    globals_dict = {
        '__file__': run_file_name,
        '__name__': '__main__',
        '__package__': None,
        '__cached__': None,
    }

    exec(code, globals_dict)


class VirtualDict(object):

    def __init__(self):
        self.var_names = []

    def __getitem__(self, key):
        self.var_names.append(key)
        return None