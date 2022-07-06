# PyMigBench
Library migration is the process of replacing one library with another in a client project.
_PyMigBench_ is a benchmark of Python Library Migration that we developed in the paper:
> Mohayeminul Islam, Ajay Kumar Jha, Sarah Nadi.
> PyMigBench and PyMigTax: A Benchmark and Taxonomy for Python Library Migration.
> _arXiv preprint arXiv:2207.01124. 2022 July 3_.

Other than the benchmark, we also developed _PyMigTax_,
a taxonomy of the migration related code changes that we include in PyMigBench.
Please read the [paper](https://arxiv.org/abs/2207.01124) to learn more about PyMigBench and PyMigTax.

This repository contains the benchmark data and the tools to explore the data.

## The dataset
The dataset is in the `data` folder. There are three main types of data: 
analogous library pairs, migrations and migration-related code changes.
Details about the dataset is in the [dataset](dataset) page.

## The tool
We provide a command line tool to easily access the dataset.
The source code of the tool is in the `code` folder.
The installation process and the syntax of the tool is in the [tool](tool) page.

## Examples
Please check the [examples](examples) page to find some use cases of the tool.
