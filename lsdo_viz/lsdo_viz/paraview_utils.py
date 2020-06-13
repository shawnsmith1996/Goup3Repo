import numpy as np

from subprocess import call


def write_paraview(script_name, image_name, quality=100, width=1000, height=1000):
    script_py_name = '{}.py'.format(script_name)
    script_py_new_name = '{}_new.py'.format(script_name)

    call(['cp', script_py_name, script_py_new_name])

    with open(script_py_new_name, 'a') as f:
        f.write('\nrenderView1.ViewSize = [{}, {}]'.format(width, height))
        f.write('\nSaveScreenshot("{}.png", GetActiveView(), magnification=5, quality={}, view=renderView1)'.format(image_name, quality))

    call(['python', script_py_new_name])