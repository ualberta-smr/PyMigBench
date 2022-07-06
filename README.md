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


## Dataset
The data is in the [data](/../../tree/main/data) folder.
There are three types of data: Analogous library pairs, valid migrations, migration-related code changes located in 
[data/libpair](/../../tree/main/data/libpair), [data/migration](/../../tree/main/data/migration) 
and [data/codechange](/../../tree/main/data/codechange) folders respectively.
Each YAML files in these folders contain information about one item.
For example, [0a65bcc_raven,sentry-sdk.yaml](/../../tree/main/data/migration) file include information about migration from _raven_ to _sentry-sdk_ in commit [0a65bcc](https://github.com/habitissimo/myaas/commit/0a65bcc).
Additionally, [data/codefile](/../../tree/main/data/codefile) contains the diffs and the old and new version of Python files modified during migrations.

# Install
1. Install the latest version of Python from [here](https://www.python.org/)
2. You can either clone the repository or 
download it from [here](https://github.com/ualberta-smr/PyMigBench/archive/refs/heads/main.zip) 
and extract it.
3. Open command prompt and move to the `code` folder.
This is the folder where you will find a `requirements.txt` file.
4. Install the dependencies. Run `pip install -r requirements.txt`

If there is no error, run `python pymigbench.py`. You should see the following output:
```yaml
count: 1
items:
- library pair: 59
  migration: 157
  code change: 436
```

# Querying
The syntax for querying PyMigBench is:
```bash
python pymigbench.py <query> -dt <data-types> -f <filters> -o <output-format>
```

* _query_: There are three query options: `c` or `count`, `l` or `list` and `d` or `detail`.
  Default is `count`.
* `-d`, `-dt`, `--data-types`: Four options: `all`,`lp` or `library-pair`,`mg` or `migration`,`cc` or `code-change`. 
Specifies the data types on which to query. 
A `count` allows multiple data types and `all` is default.
The other queries accept just one mandatory data type, no defaults.
The `list` query returns a list of IDs, and the `detail` returns the items in JSON format. 
* `-f`, `--filters`: You can pass zero or more filters to all queries.
Each filter must be in the format `<attribute>=<value>`.
Here, `attribute` is a property/attribute of a data type.
Please open a `yaml` file in `data` folder to find the property names.
We assume all attributes to be string or list of string.
The `value` is therefore any string that will be matched against the attribute.
The value accepts matching by `!`, `?` and `*` through [fnmatch.fnmatch](https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch). 
For list properties, a data is returned if at least one of the list item satisfies the filter.
See the examples for better understanding the filters.
* `-o`, `--output-format`: The format in which the result will be shown. Currently, supports YAML and JSON. Default YAML.
* `-h`, `--help`: show help.

The result is printed in JSON format.

# Examples
#### Get a count of all data:  

`python pymigbench.py count -dt all` or `python pymigbench.py`
```yaml
count: 1
items:
- library pair: 59
  migration: 157
  code change: 436
```
#### Get count of _code changes_ and _migrations_:
```bash
python pymigbench.py -dt cc mg
```  
```yaml
count: 1
items:
- code change: 436
  migration: 157
```
#### List all _code changes_: 
```bash
python pymigbench.py list -dt cc
```
```yaml
count: 436
items:
- '100_1'
- '101_1'
- '102_1'
# (400+ items hidden for brevity)
- '98_1'
- '99_1'
- '9_1'
```
#### List all _code changes_ having _function call_ replacement:   
```bash 
python pymigbench.py list -dt cc -f program_element="function call"
```
```yaml
count: 155
items:
- '101_1'
- '102_1'
- '104_1'
# (100+ items hidden for brevity)
- '93_1'
- '96_1'
- '97_1'
```
#### List all _code changes_ having _one-to-many_ _function call_ replacement:
```bash 
python pymigbench.py list -dt cc -f program_element="function call" cardinality="1-n"
```
```yaml
count: 13
items:
- '109_1'
- '12_1'
- '12_2'
- '175_1'
- '175_2'
- '201_1'
- '203_1'
- '204_1'
- '207_1'
- '211_1'
- '214_1'
- '96_1'
- '97_1'
```
#### Find all _migrations_ to target library _aiohttp_:
```bash
python pymigbench.py list -dt mg -f target=aiohttp
```
```yaml
count: 11
items:
- 1c574c1_requests,aiohttp
- 1d8923a_requests,aiohttp
- 45d94dd_gcloud-aio-core,aiohttp
- 53f2073_requests,aiohttp
- 6e7ee63_requests,aiohttp
- 963f347_gcloud-aio-core,aiohttp
- a5c04bb_requests,aiohttp
- ab4e5fd_requests,aiohttp
- b2c9313_requests,aiohttp
- d15540f_gcloud-aio-core,aiohttp
- d3a9a16_requests,aiohttp
```

#### Get details of _code changes_ from _requests_ to _aiohttp_ having an argument change (add, delete or transform)
```bash
python pymigbench.py detail -dt cc -f source=requests target=aiohttp program_element="function call" properties="arg*"
```
In this query, we use the knowledge that attribute addition, attribute deletion and attribute transformation starts with
`arg` and no other properties start with `arg`. 
```yaml
count: 4
items:
- id: '201_1'
  repo: raptor123471/dingolingo
  commit: 1d8923abae93915ad877774e0fdc812d6c53a70b
  source: requests
  target: aiohttp
  pair_id: requests,aiohttp
  filepath: musicbot/linkutils.py
  program_element: function call
  cardinality: 1-n
  properties:
  - argument addition
  - making async
  source_version_line: '35'
  target_version_line: 36-37
- id: '203_1'
  repo: raptor123471/dingolingo
  commit: 1d8923abae93915ad877774e0fdc812d6c53a70b
  source: requests
  target: aiohttp
  pair_id: requests,aiohttp
  filepath: musicbot/linkutils.py
  program_element: function call
  cardinality: 1-n
  properties:
  - argument transformation
  - making async
  source_version_line: '98'
  target_version_line: 100-101
- id: '216_1'
  repo: ictu/quality-time
  commit: d3a9a16a72348cece48c9788cf10db6cc043ec7c
  source: requests
  target: aiohttp
  pair_id: requests,aiohttp
  filepath: components/collector/src/base_collectors/source_collector.py
  program_element: function call
  cardinality: 1-1
  properties:
  - argument deletion
  - argument transformation
  source_version_line: '106'
  target_version_line: '101'
- id: '222_1'
  repo: ictu/quality-time
  commit: d3a9a16a72348cece48c9788cf10db6cc043ec7c
  source: requests
  target: aiohttp
  pair_id: requests,aiohttp
  filepath: components/collector/src/source_collectors/api_source_collectors/azure_devops.py
  program_element: function call
  cardinality: 1-1
  properties:
  - argument deletion
  - making await
  source_version_line: '31'
  target_version_line: '31'
```