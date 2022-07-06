# The dataset
## The PyMigBench dataset
The data is in the [data](/../../tree/main/data) folder.
There are three types of data: Analogous library pairs, valid migrations, migration-related code changes located in 
[data/libpair](/../../tree/main/data/libpair), [data/migration](/../../tree/main/data/migration) 
and [data/codechange](/../../tree/main/data/codechange) folders respectively.
Each YAML files in these folders contain information about one item.
For example, [0a65bcc_raven,sentry-sdk.yaml](/../../tree/main/data/migration) file include information about migration from _raven_ to _sentry-sdk_ in commit [0a65bcc](https://github.com/habitissimo/myaas/commit/0a65bcc).
Additionally, [data/codefile](/../../tree/main/data/codefile) contains the diffs and the old and new version of Python files modified during migrations.