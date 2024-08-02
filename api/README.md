This is a library to access the PyMigBench dataset.
Visit the [GitHub repository](https://github.com/ualberta-smr/pymigbench) to learn about the dataset.

## Installation
The library and the dataset should be at the same version to be compatible.
To install the library, run:
```bash
pip install pymigbench==<version>
```

## Usage
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



  
