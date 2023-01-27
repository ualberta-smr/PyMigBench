---
nav_order: 1
---
# PyMigBench dataset
The PyMigBench dataset is in the [data]({{ site.vars.repo }}/tree/msr-2023-datatrack/data){:target="_blank"} directory.
There are two types of data: analogous library pairs and valid migrations located in `libpair` and `migration` subdirectories respectively.
Each YAML file in the `libpair` and `migration` folders contain information about one data item.
Additionally, the `codefile` subdirectory has the diff files of the code changes, and the code files before and after migration.

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
Migration from flask to quart at commit 0a70f2b: [0a70f2b_flask,quart.yaml]({{ site.vars.repo }}/blob/main/data/migration/0a70f2b_flask,quart.yaml){:target="_blank"}
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

### Sample diff file
The below diff file shows the changes in the `app/run.py` in the migration mentioned above: [pgjones@faster_than_flask_article__0a70f2b__app$run.py.diff]({{ site.vars.repo }}/blob/main/data/codefile/pgjones@faster_than_flask_article__0a70f2b__app$run.py.diff).
The diff file file name formate is: `{repouser}@{reponame}__{8_characters_commit_hash}__{filepath-in-repo}.diff`.
The slash (`/`) or backslash (`\`) in the file path is replaced with a dollar (`$`) sign.
 
```diff
diff --git a/app/run.py b/app/run.py
        index 253538aa8cd65a3ed48563c2ea4594d998286293..0a70f2bddae90da13da5bce2b77ea56355ecc5d1 100644
        --- a/app/run.py
        +++ b/app/run.py
@@ -1,44 +1,21 @@
 import os
 from contextlib import contextmanager
 
-from flask import Flask
-from psycopg2.extras import RealDictCursor
-from psycopg2.pool import ThreadedConnectionPool
+import asyncpg
+from quart import Quart
 
 from films import blueprint as films_blueprint
 from reviews import blueprint as reviews_blueprint
 
 
-class PoolWrapper:
-    """Exists to provide an acquire method for easy usage.
-
-        pool = PoolWrapper(...)
-        with pool.acquire() as conneciton:
-            connection.execute(...)
-    """
-
-    def __init__(self, max_pool_size: int, *, dsn):
-        self._pool = ThreadedConnectionPool(
-            1, max_pool_size, dsn=dsn, cursor_factory=RealDictCursor,
-        )
-
-    @contextmanager
-    def acquire(self):
-        try:
-            connection = self._pool.getconn()
-            yield connection
-        finally:
-            self._pool.putconn(connection)
-
-
 def create_app():
-    app = Flask(__name__)
+    app = Quart(__name__)
     app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
 
     @app.before_first_request
-    def create_db():
-        dsn = 'host=0.0.0.0 port=5432 dbname=dvdrental user=dvdrental password=dvdrental'
-        app.pool = PoolWrapper(20, dsn=dsn)  #os.environ['DB_DSN'])
+    async def create_db():
+        dsn = 'postgres://dvdrental:dvdrental@0.0.0.0:5432/dvdrental'
+        app.pool = await asyncpg.create_pool(dsn, max_size=20)  #os.environ['DB_DSN'])
 
     app.register_blueprint(films_blueprint)
     app.register_blueprint(reviews_blueprint)
```
