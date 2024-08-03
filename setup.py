from setuptools import setup

setup(
    name='pymigbench',
    description='APIs to access the PyMigBench dataset',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    version="2.2.4",
    packages=['pymigbench'],
    author='PyMigBench Team',
    author_email='mohayemin@ualberta.ca',
    url='https://github.com/ualberta-smr/pymigbench',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.11',
    install_requires=[
        'pyyaml~=6.0',
    ],
)
