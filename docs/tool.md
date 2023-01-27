---
nav_order: 2
---
# PyMigBench tool
The repository contains a command line tool to easily query the benchmark.
The source code of the tool is in the [code]({{ site.vars.repo }}/tree/msr-2023-datatrack/code){:target="_blank"} folder.

## Install
1. Install Python from [here](https://www.python.org/). We developed the tool in Python 3.11.0, but a later version should also work.
2. Clone the [repository]({{site.vars.repo}}){:target="_blank"} and checkout to `msr-2023-datatrack` branch. Alternatively, 
[download the zip](https://github.com/ualberta-smr/PyMigBench/archive/refs/heads/msr-2023-datatrack.zip) 
and extract it.
1. Open a terminal and change the directory to the `code` folder.
This is the folder where you will find a `requirements.txt` file.
4. Install the dependencies. Run `pip install -r requirements.txt`

If there is no error, run `python pymigbench.py` to check if it is working. You should see an output similar to the one below:
```yaml
- analogous library pairs: 59
  unique libraries: 99
  unique source libraries: 55
  unique target libraries: 56
  unique library domains: 13
  migrations: 157
  client repositories having migrations: 127
  library pairs having migrations: 49
  migration commits: 155
  migrations having code changes: 75
  library pairs having code changes: 34
  client repositories having code changes: 57
  commits having code changes: 74
  modified files: 161
  modified code segments: 375
```

## Query PyMigBench
The syntax for querying PyMigBench is:
```bash
python pymigbench.py <query> -dt <data-types> -f <filters> -o <output-format>
```

* _query_: There are four query options: `s` or `summary`, `l` or `list` and `d` or `detail`,  `c` or `count`.
  Default is `summary`.
    - `summary` returns the summary of the dataset.
    - `list` returns the list if IDs.
    - `detail` returns the a list of data items that include all of its properties.
    - `count` returns only the number of data items, no data.
* `-d`, `-dt`, `--data-types`: Specifies the data types on which to query. Can be either `lp` or `library-pair` OR `mg` or `migration`. 
A `summary` query does not accept any data types.
The other queries accept one mandatory data type.
* `-f`, `--filters`: You can pass zero or more filters to all queries except for summary.
Each filter must be in the format `<property>=<value>`.
Here, `property` is a property of a data type.
Please check the [property values](#property) section below for a list of frequently used properties and their possible values.
Check the [dataset](dataset) page for the full schema of the dataset.
The properties are of type string, list of string, or list of objects.
The `value` is therefore any string that will be matched against the property.
The value accepts matching by `!`, `?` and `*` through [fnmatch.fnmatch](https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch){:target="_blank"}. 
For array type properties, a data is returned if at least one of the list item satisfies the filter.
Summary ignores the filters.
* `-o`, `--output-format`: The format in which the result will be shown. Currently, supports YAML and JSON. Default YAML.
* `-h`, `--help`: show help.

Visit the [Examples](examples) page to check some use cases of the tool.
Feel free to [ask for help](https://github.com/ualberta-smr/PyMigBench/issues/new?template=query-help.md){:target="_blank"} in writing a query.


## <a name="property"></a> Property values
### Property `repo` in migration data type
- agdsn/sipa
- alice-biometrics/petisco
- apryor6/flaskerize
- azure/aztk
- bcgov/gwells
- bcgov/theorgbook
- biznetgio/restknot
- bretttolbert/verbecc-svc
- camptocamp/c2cgeoportal
- cloud-custodian/cloud-custodian
- common-workflow-language/cwltool
- duanhongyi/dwebsocket
- elblogbruno/notionai-mymind
- freeopcua/opcua-asyncio
- habitissimo/myaas
- hhyo/archery
- holgern/beem
- ictu/quality-time
- intel/stacks-usecase
- intelai/inference-model-manager
- kizniche/mycodo
- learningorchestra/learningorchestra
- lonelam/onlinejudgeshu
- malwaredllc/byob
- microsoft/nni
- milvus-io/bootcamp
- nlpia/nlpia-bot
- oddluck/limnoria-plugins
- opengisch/qfieldcloud
- openstack/oslo.messaging
- orchest/orchest
- pgjones/faster_than_flask_article
- pokainc/cfn-cross-region-export
- pythondataintegrator/pythondataintegrator
- raptor123471/dingolingo
- rcos/observatory-retired
- rocketmap/rocketmap
- sapfir0/premier-eye
- shoebot/shoebot
- slackapi/python-slack-events-api
- slackapi/python-slack-sdk
- snemes/malware-analysis
- stefal/rtkbase
- synesthesiam/voice2json
- talkiq/gcloud-aio
- talkpython/async-techniques-python-course
- testdrivenio/flask-react-aws
- thespaghettidetective/thespaghettidetective
- thombashi/datetimerange
- thombashi/pingparsing
- thombashi/sqlitebiter
- thombashi/tcconfig
- toufool/auto-split
- virtuber/openvtuber
- weasyl/weasyl
- ziirish/burp-ui
- zulip/python-zulip-api


### Property `source` and `target` in migration and library pair data types
- aiohttp
- argparse
- bcrypt
- celery
- configargparse
- confluent-kafka
- cryptography
- dataproperty
- django-rest-swagger
- drf-yasg
- eventlet
- fastapi
- fasteners
- flask
- flask-restful
- flask-restplus
- flask-restx
- fuzzywuzzy
- gcloud-aio-core
- gevent
- huey
- kafka-python
- ldap3
- lockfile
- logbook
- loguru
- openpyxl
- pendulum
- pil
- pillow
- py-bcrypt
- pycrypto
- pycryptodome
- pycryptodomex
- pymilvus
- pymilvus-orm
- pyqt5
- pyside6
- python-ldap
- pytz
- pyyaml
- quart
- rapidfuzz
- raven
- requests
- retrying
- rq
- ruamel.yaml
- sentry-sdk
- slack-sdk
- slackclient
- tenacity
- typepy
- uvicorn
- xlsxwriter


### Property `domain` in library pair data type
- API wrapper
- Cryptography
- Data processing
- Database client
- Development framework/extension
- File reader/writer
- HTTP client/server
- Image processing
- Logging/tracing
- Machine learning
- Multitasking/multiprocessing
- Networking
- Utilities

