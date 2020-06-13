import numpy as np
import os 
from stl import mesh


def get_sphere_triangulation(radius, num_az, num_el):
    """
    Get a triangulation of a sphere.
    This function returns an array that can be fed into write_stl_triangles.
    """
    lins_el = np.linspace(0, np.pi, num_el)
    lins_az = np.linspace(0, 2 * np.pi, num_az)

    ones_el = np.ones(num_el)
    ones_az = np.ones(num_az)

    el = np.outer(lins_el, ones_az)
    az = np.outer(ones_el, lins_az)

    xyz = np.empty((num_el, num_az, 3))
    xyz[:, :, 0] = radius * np.sin(el) * np.cos(az)
    xyz[:, :, 1] = radius * np.sin(el) * np.sin(az)
    xyz[:, :, 2] = radius * np.cos(el)

    num_triangles_1 = (num_el - 3) * (num_az - 1)
    num_triangles_2 = (num_az - 1)
    num_triangles = 2 * num_triangles_1 + 2 * num_triangles_2

    data = np.empty((num_triangles, 3, 3))
    ind1 = 0
    ind2 = 0

    ind2 += num_triangles_1
    for k in range(3):
        data[ind1:ind2, 0, k] = xyz[1:-2, 1:  , k].flatten()
        data[ind1:ind2, 1, k] = xyz[2:-1, 0:-1, k].flatten()
        data[ind1:ind2, 2, k] = xyz[1:-2, 0:-1, k].flatten()
    ind1 += num_triangles_1

    ind2 += num_triangles_1
    for k in range(3):
        data[ind1:ind2, 0, k] = xyz[1:-2, 1:  , k].flatten()
        data[ind1:ind2, 1, k] = xyz[2:-1, 0:-1, k].flatten()
        data[ind1:ind2, 2, k] = xyz[2:-1, 1:  , k].flatten()
    ind1 += num_triangles_1

    ind2 += num_triangles_2
    for k in range(3):
        data[ind1:ind2, 0, k] = xyz[1, 1:  , k].flatten()
        data[ind1:ind2, 1, k] = xyz[1, 0:-1, k].flatten()
        data[ind1:ind2, 2, k] = xyz[0, 0:-1, k].flatten()
    ind1 += num_triangles_2

    ind2 += num_triangles_2
    for k in range(3):
        data[ind1:ind2, 0, k] = xyz[-2, 1:  , k].flatten()
        data[ind1:ind2, 1, k] = xyz[-2, 0:-1, k].flatten()
        data[ind1:ind2, 2, k] = xyz[-1, 1:  , k].flatten()
    ind1 += num_triangles_2

    return data


def get_earth_triangulation(radius):
    """
    Get a triangulation of the Earth with land raised slightly above regions covered with water.
    This function returns an array that can be fed into write_stl_triangles.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    data = read_stl_triangles('{}/earth_topographic'.format(dir_path))
    norms = np.linalg.norm(data, axis=2)
    average_radius = np.sum(norms) / np.prod(norms.shape)
    data /= average_radius
    data *= radius
    return data


def write_stl_triangles(stl_file_name, data):
    """
    Write an STL file from a triangulation given as an array of shape [nt, 3, 3].
    The first 3 refers to the vertices of each triangle.
    The second 3 is for x-y-z.
    """
    cube = mesh.Mesh(np.zeros(data.shape[0], dtype=mesh.Mesh.dtype))
    cube.vectors[:, :, :] = data
    cube.save('{}.stl'.format(stl_file_name))


def read_stl_triangles(stl_file_name):
    """
    Read an STL file and return the triangulation as an array of shape [nt, 3, 3].
    The first 3 refers to the vertices of each triangle.
    The second 3 is for x-y-z.
    """
    return mesh.Mesh.from_file('{}.stl'.format(stl_file_name)).vectors


def write_stl_structured_list(stl_file_name, data_list):
    """
    Write an STL file from a list of arrays of shape [ni, nj, 3].
    """
    if not isinstance(data_list, list):
        data_list = [data_list]

    triangles_list = []
    for data in data_list:
        nx = data.shape[0] - 1
        ny = data.shape[1] - 1

        triangles = np.empty((nx, ny, 3, 3))
        triangles[:, :, 0, :] = data[ :-1,1:  , :]
        triangles[:, :, 1, :] = data[1:  , :-1, :]
        triangles[:, :, 2, :] = data[1:  ,1:, :]
        triangles = triangles.reshape((nx * ny, 3, 3))
        triangles_list.append(triangles)

        triangles = np.empty((nx, ny, 3, 3))
        triangles[:, :, 0, :] = data[ :-1,1:  , :]
        triangles[:, :, 1, :] = data[1:  , :-1, :]
        triangles[:, :, 2, :] = data[ :-1, :-1, :]
        triangles = triangles.reshape((nx * ny, 3, 3))
        triangles_list.append(triangles)

    triangles = np.concatenate(triangles_list)

    write_stl_triangles(stl_file_name, triangles)