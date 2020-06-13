import numpy as np
from stl import mesh


def write_tecplot_dat(dat_file_name, data, num_i, num_j, num_k, var_name='Field'):
    """
    Write a Tecplot dat file where data is an array of shape n x 3.
    The length of this array, n, should be the product of num_i, num_j, num_k.
    """
    if data.shape[1] == 3:
        data = np.concatenate(
            [data, np.zeros((data.shape[0], 1))],
            axis=1,
        )
    with open('{}.dat'.format(dat_file_name), 'w') as f:
        f.write('TITLE = "{}"\n'.format(dat_file_name))
        f.write('VARIABLES = "X", "Y", "Z"\n')
        f.write('ZONE I={}, J={}, K={}, DATAPACKING=POINT\n'.format(num_i, num_j, num_k))
        for ind in range(data.shape[0]):
            f.write('{} {} {}\n'.format(data[ind, 0], data[ind, 1], data[ind, 2]))
            # f.write('{} {} {} {}\n'.format(data[ind, 0], data[ind, 1], data[ind, 2], data[ind, 3]))


def write_tecplot_dat_curve(dat_file_name, data, var_name='Field'):
    """
    Write a Tecplot dat file for a 3-D curve where data is an array of shape n x 3.
    """
    write_tecplot_dat(dat_file_name, data, 1, data.shape[0], 1, var_name=var_name)