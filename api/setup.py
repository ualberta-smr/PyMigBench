from setuptools import setup

setup(
    name='pymigbench',
    description='APIs to access the PyMigBench dataset',
    version='0.0.1',
    packages=['pymigbench'],
    author='PyMigBench Team',
    author_email='mohayemin@ualberta.ca',
    url='https://github.com/ualberta-smr/pymigbench',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System:: OSIndependent',
    ],
    python_requires='>=3.11',
    install_requires=[
        'pyyaml~=6.0',
    ],
)
