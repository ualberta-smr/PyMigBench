---
nav_order: 1
---
# PyMigBench dataset
The PyMigBench dataset is in the [data]({{ site.vars.repo }}/tree/main/data){:target="_blank"} directory.
There are three types of data: analogous library pairs, valid migrations, and migration-related code changes located in respective subdirectories.
Each YAML file in these subdirectories contains information about one data item.

## Library pair
* Location: [data/libpair]({{ site.vars.repo }}/tree/main/data/libpair){:target="_blank"}


### Schema
- `id`: unique ID of the library pair
- `source`: the source library
- `target`: the target library
- `domain`: the domain of the library pair

### Sample data file
Analogous library pair from flask to quart: [flask,quart.yaml]({{ site.vars.repo }}/blob/main/data/libpair/flask,quart.yaml){:target="_blank"}
```yaml
id: flask,quart
source: flask
target: quart
domain: Development framework/extension
```

## Migration
* Location: [data/migration]({{ site.vars.repo }}/tree/main/data/migration){:target="_blank"}

### Schema
- `id`: unique ID of the migration
- `source`: the source library
- `target`: the target library
- `repo`: the repository where the migration happened
- `commit`: the hash of the commit where the migration happened
- `pair_id`: the ID of the library pair in the migration
- `commit_message` (type: multiline text): the commit message

### Sample data file
Migration from flask to quart at commit 7ea7ddb: [7ea7ddb_flask,quart.yaml]({{ site.vars.repo }}/blob/main/data/migration/7ea7ddb_flask,quart.yaml){:target="_blank"}
```yaml
id: 7ea7ddb_flask,quart
source: flask
target: quart
repo: synesthesiam/voice2json
commit: 7ea7ddb8400775282e82c1adcb17b013f27ede2b
pair_id: flask,quart
commit_message: Using quart for web interface
```

## Migration-related code change
* Location: [data/codechange]({{ site.vars.repo }}/tree/main/data/codechange){:target="_blank"}.
Additionally, [data/codefile]({{ site.vars.repo }}/tree/main/data/codefile){:target="_blank"}
contains the diffs and the old and new version of Python files modified during migrations.

### Schema  
- `id`: unique ID of the code change
- `repo`: the repository where the code change happened
- `commit`: the hash of the commit where the code change happened
- `source`: the source library
- `target`: the target library
- `pair_id`: the ID of the library pair in the code change
- `filepath`: path of the file within the repository where the code change happened
- `program_element`: the program element affected by the code change
- `cardinality`: the cardinality of the code change
- `properties` (type: array): additional properties of the code change
- `source_version_line`: the lines in the old version of the code deleted during the migration
- `target_version_line`: the lines in the new version of the code deleted during the migration


### Sample data file
A code change from flask to quart at commit 7ea7ddb: [80_1.yaml]({{ site.vars.repo }}/blob/main/data/codechange/80_1.yaml){:target="_blank"}
```yaml
id: '80_1'
repo: synesthesiam/voice2json
commit: 7ea7ddb8400775282e82c1adcb17b013f27ede2b
source: flask
target: quart
pair_id: flask,quart
filepath: web/app.py
program_element: import
cardinality: 1-1
properties:
- module name change
- object name change
source_version_line: '20'
target_version_line: '20'
```

The part of the diff file showing the code change that the above YAML file represents: [synesthesiam@voice2json__7ea7ddb__web$app.py.diff]({{ site.vars.repo }}/blob/main/data/codefile/synesthesiam@voice2json__7ea7ddb__web$app.py.diff){:target="_blank"}
```diff
diff --git a/web/app.py b/web/app.py
        index 6917d188b5e3fa43fce79b44d4e1ec161e1443ab..7ea7ddb8400775282e82c1adcb17b013f27ede2b 100644
        --- a/web/app.py
        +++ b/web/app.py
@@ -17,15 +17,15 @@ from pathlib import Path
 from typing import Optional, Dict, Any, Tuple, BinaryIO, List
 
 import pydash
-from flask import Flask, request, render_template, send_from_directory, flash, send_file
+from quart import Quart, request, render_template, send_from_directory, flash, send_file
```
