from distutils.core import setup

setup(
    name='lsdo_viz',
    version='0',
    packages=[
        'lsdo_viz',
    ],
    install_requires=[
    ],
    entry_points="""
        [console_scripts]
        lsdo_om=lsdo_viz.main_om:main_om
        lm=lsdo_viz.main_om:main_om
        lsdo_viz=lsdo_viz.main_viz:main_viz
        lv=lsdo_viz.main_viz:main_viz
    """,
)