---
nav_order: 1
---
# PyMigBench dataset
The PyMigBench dataset is in the [data]({{ site.vars.repo }}/tree/msr-2023-datatrack/data){:target="_blank"} directory.
There are three types of data: analogous library pairs, valid migrations, and migration-related code changes located in respective subdirectories.
Each YAML file in these subdirectories contains information about one data item.

## Library pair
* Location: [data/libpair]({{ site.vars.repo }}/tree/msr-2023-datatrack/data/libpair){:target="_blank"}


### Schema
- `id`: unique ID of the library pair
- `source`: the source library
- `target`: the target library
- `domain`: the domain of the library pair

### Sample data file
Analogous library pair from flask to quart: [flask,quart.yaml]({{ site.vars.repo }}/blob/msr-2023-datatrack/data/libpair/flask,quart.yaml){:target="_blank"}
```yaml
id: flask,quart
source: flask
target: quart
domain: Development framework/extension
```

## Migration
* Location: [data/migration]({{ site.vars.repo }}/tree/msr-2023-datatrack/data/migration){:target="_blank"}

### Schema
- `id`: unique ID of the migration
- `source`: the source library
- `target`: the target library
- `repo`: the repository where the migration happened
- `commit`: the hash of the commit where the migration happened
- `pair_id`: the ID of the library pair in the migration
- `commit_message` (type: multiline text): the commit message
- `commit_url`: URL of the migration commit on GitHub
- `code_changes` (type: list): the list of code changes found in this migration.
  - `filepath`: the file where the code was changed
  - `lines`: a list of range of line numbers where the code was changed for migration.

### Sample data file
Migration from flask to quart at commit 0a70f2b: [0a70f2b_flask,quart.yaml]({{ site.vars.repo }}/blob/msr-2023-datatrack/data/migration/0a70f2b_flask,quart.yaml){:target="_blank"}
```yaml
id: 0a70f2b_flask,quart
source: flask
target: quart
repo: pgjones/faster_than_flask_article
commit: 0a70f2bddae90da13da5bce2b77ea56355ecc5d1
pair_id: flask,quart
commit_message: Quart version
commit_url: https://github.com/pgjones/faster_than_flask_article/commit/0a70f2bd
code_changes:
- filepath: app/films.py
  lines:
  - '1:1'
- filepath: app/run.py
  lines:
  - '4:5'
  - '35:12'
- filepath: app/reviews.py
  lines:
  - '1:1'
  - '8:8'

```
