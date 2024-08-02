from setuptools import setup

setup(
    name='pymigbench',
    description='APIs to access the PyMigBench dataset',
    version='0.1',
    packages=['pymigbench'],
    install_requires=[
        'pyyaml~=6.0',
    ],
)
