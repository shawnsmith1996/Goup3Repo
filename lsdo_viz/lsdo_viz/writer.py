import os
import glob

from lsdo_utils.api import OptionsDictionary

from lsdo_viz.utils import make_dir, get_new_file_path, clean, get_numbered_file_name

try:
    import cPickle as pickle
except:
    import pickle


class Writer(object):

    def __init__(self, data_dir='_data', data_file_name='opt', system=None, var_names=None):
        # Current working directory
        working_dir_path = os.getcwd()
        working_dir_path = working_dir_path.replace(r'\\ ', r'\ ')
        working_dir_path = working_dir_path.replace(r'\ ', r' ')
        self.working_dir_path = working_dir_path

        # Data directory
        self.data_dir = data_dir

        # File name
        self.data_file_name = data_file_name

        # System
        self.system = system

        # Variable names
        self.var_names = var_names

        # Make data directory if it doesn't exist
        make_dir(data_dir)

    def clean(self):
        """
        Delete all files in data directory.
        """
        clean(self.data_dir)

    def write(self):
        """
        Write data currently in OpenMDAO system instance to file, with next available number.
        """
        data_dict = dict()
        for var_name in self.var_names:
            data_dict[var_name] = self.system._outputs[var_name]

        abs_file_path = get_new_file_path(self.data_dir, self.data_file_name, 'pkl')[0]
        with open(abs_file_path, 'wb') as handle:
            pickle.dump(data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def read(self, load_ind=None):
        """
        Read all files and return a list of dictionaries.
        """
        data_dict_list = []

        ind = 0
        while True:
            abs_file_path = r'{0}/{1}/{2}'.format(
                self.working_dir_path, 
                self.data_dir, 
                get_numbered_file_name(
                    self.data_file_name, 
                    ind,
                    'pkl',
                ),
            )
            if not os.path.isfile(abs_file_path):
                break

            with open(abs_file_path, 'rb') as handle:
                data_dict = pickle.load(handle)

            data_dict_list.append(data_dict)

            ind += 1

        if load_ind is not None:
            data_dict = data_dict_list[load_ind]
            for var_name in self.var_names:
                try:
                    self.system._outputs[var_name] = data_dict[var_name]
                except:
                    pass
            
        return data_dict_list