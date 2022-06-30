# PyMigBench
This repository contains the dataset of PyMigBench and the tools to explore the dataset.
The dataset is in the `data` folder and the tool is in the `code` folder.

# Install
1. Install the latest version of Python from [here](https://www.python.org/)
2. You can either clone the repository or 
download it from [here](https://github.com/ualberta-smr/PyMigBench/archive/refs/heads/main.zip) 
and extract it.
3. Open command prompt and move to the `code` folder.
This is the folder where you will find a `requirements.txt` file.
4. Install the dependencies. Run `pip install -r requirements.txt`

If there is no error, run `python pymigbench.py`. You should see the following output:
```
59 library pair
157 migration
436 code change
```

# Examples
The syntax for querying PyMigBench is:
```bash
python pymigbench.py <query> -dt <data-types> -f <filters>
```
You can use three types of queries: 
`c` or `count`, `l` or `list` and `d` or `detail`.
The data types can be `lp` (library pair), `mg` (migration) and `cc` (code change).
You can also use `all` to get results for all data types.

## Count
1. Get a count of all data:
```bash
python pymigbench.py count -dt all
```
`count` is the default query and `all` is the default data type for count.
That means the above query is equivalent to just `python pymigbench.py`.
Both will show: 
```
59 library pair
157 migration
436 code change
```
2. Get count of `code changes` and `migrations`: `python pymigbench.py -dt cc mg`.

