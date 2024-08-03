PyMigBench is a benchmark of Python Library Migrations. 
This repository contains the data and the code the library that can be used to access the dataset.

## Dataset
### PyMigBench v2
The current version, PyMigBench-2.0, includes 3,096 migration-related code changes from 335 migrations between 141 analogous library pairs.
This includes all migrations from [PyMigBench v1](#pymigbench-v1) and additional migrations borrowed from the [SALM dataset](https://ieeexplore.ieee.org/document/10123560).
The data also includes additional information per migration-related code change compared to v1.

The dataset is published through the FSE 2024 paper titled *Characterizing Python Library Migrations*.
We will add the citation info once it is available.
[Release 2.0.2](https://github.com/ualberta-smr/PyMigBench/releases/v2.0.2) points to the exact dataset linked to the paper.
The data is also permanently archived in [figshare](https://doi.org/10.6084/m9.figshare.24216858.v2).
Use either of these links to reproduce the paper.

We may update this repository to correct any mistakes or add more data and it may not synch with the paper.
For, the latest data, use the [latest release](https://github.com/ualberta-smr/PyMigBench/releases/latest) in this repository.

### PyMigBench v1
We recommend using PyMigBench v2 for any new research.
However, you want to use the v1 dataset, you should look at [Release 1.0.3](https://github.com/ualberta-smr/PyMigBench/releases/v1.0.3).
Cite the paper below if you use the v1 dataset.

```
@INPROCEEDINGS{pymigbench,
  author={Islam, Mohayeminul and Jha, Ajay Kumar and Nadi, Sarah and Akhmetov, Ildar},
  booktitle={2023 IEEE/ACM 20th International Conference on Mining Software Repositories (MSR)}, 
  title={PyMigBench: A Benchmark for Python Library Migration}, 
  year={2023},
  volume={},
  number={},
  pages={511-515},
  doi={10.1109/MSR59073.2023.00075}
}
```


## Library

### Installation
The library and the dataset should be at the same version to be compatible.
To install the library, run:
```bash
pip install pymigbench==<version>
```

### Basic usage
To use the library, you need to have the dataset downloaded.
You can download the dataset from the [GitHub repository](https://github.com/ualberta-smr/pymigbench).

```python
from pymigbench.database import Database
from pathlib import Path

yaml_root = Path('repo-root/migration/')

db = Database.load_from_dir(yaml_root)  # Load the dataset from the directory
migs = db.migs()  # Get all the migrations
```

### The constants
There are several enums to help you work with the dataset:
They are all in the `pymigbench.constants` module. Example: 
```python
from pymigbench.constants import ProgramElement
```

### The migration-related objects
There are three main classes to encapsulate the data: `Migration`, `MigrationFile`, and `CodeChange`.

`Migration` is the top level class representing one single migration, ie, one yaml file.
`Migration` has a list of `MigrationFile` objects, which represent the files that were changed in the migration.
`MigrationFile` has a list of `CodeChange` objects, which represent a single migration-related code change.
Each of these model classes has an `id()` method that returns a unique identifier for the object across the full dataset.
`CodeChange` object additionally has an `index` property and a `id_in_file()` method, which are unique within container file.
Each of the classes has some additional helper methods.

 



## Contributors
- [Mohayeminul Islam](https://mohayemin.github.io/)
- [Ajay Kumar Jha](https://hifromajay.github.io/)
- [Sarah Nadi](https://sarahnadi.org/)
- [Ildar Akhmetov](https://ildarakhmetov.com/)  

For any queries, please contact mohayemin@ualberta.ca.