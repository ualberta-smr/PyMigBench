---
nav_order: 2
---
# PyMigBench tool
The repository contains a command line tool to easily query the benchmark.
The source code of the tool is in the [code]({{ site.vars.repo }}/tree/main/code){:target="_blank"} folder.

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
Each filter must be in the format `<property>=<value>`.
Here, `property` is a property of a data type.
Please check the [property values](#property) section below for a list of possible property values.
We assume all attributes to be string or array of string.
The `value` is therefore any string that will be matched against the attribute.
The value accepts matching by `!`, `?` and `*` through [fnmatch.fnmatch](https://docs.python.org/3/library/fnmatch.html#fnmatch.fnmatch){:target="_blank"}. 
For array type properties, a data is returned if at least one of the list item satisfies the filter.
See the [examples](examples) for better understanding the filters.
* `-o`, `--output-format`: The format in which the result will be shown. Currently, supports YAML and JSON. Default YAML.
* `-h`, `--help`: show help.

Visit the [Examples](examples) page to check some use cases of the tool.


## <a name="property"></a> Property values
1. `program_element`
    - attribute access
    - decorator
    - function call
    - import
2. `cardinality`
    - 1-1
    - 1-n
    - n-1
    - n-n
3. `properties` (array type)
    - *empty array*. Specify using an empty string (`properties=""`) in filter.
    - argument addition
    - argument deletion
    - argument transformation
    - attribute name change
    - changing to method call
    - decorator name change
    - full statement replacement
    - function name change
    - making async
    - making await
    - module name change
    - object name change 
4. `repo`
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
5. `source`/`target`
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
