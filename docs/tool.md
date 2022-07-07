---
nav_order: 2
---
# PyMigBench tool
The repository contains a command line tool to easily query the benchmark.
The source code of the tool is in the [code]({{ site.vars.repo }}/tree/main/code) folder.

## Install
1. Install Python from [here](https://www.python.org/). We developed the tool in Python 3.10.0, but a later version should also work.
2. Either clone the [repository]({{site.vars.repo}}){:target="_blank"} or 
download it from [here](https://github.com/ualberta-smr/PyMigBench/archive/refs/heads/main.zip) 
and extract it.
3. Open a terminal and change the directory to the `code` folder.
This is the folder where you will find a `requirements.txt` file.
4. Install the dependencies. Run `pip install -r requirements.txt`

If there is no error, run `python pymigbench.py` to check if it is working. You should see the following output:
```yaml
count: 1
items:
- library pair: 59
  migration: 157
  code change: 436
```

## Syntax
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
The value accepts matching by `!`, `?` and `*` through [fnmatch.fnmatch](https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch){:target="_blank"}. 
For array type properties, a data is returned if at least one of the list item satisfies the filter.
See the [examples](examples) for better understanding the filters.
* `-o`, `--output-format`: The format in which the result will be shown. Currently, supports YAML and JSON. Default YAML.
* `-h`, `--help`: show help.

Visit the [Examples](examples) page to check some use cases of the tool.
