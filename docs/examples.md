---
nav_order: 3
---
# PyMigBench query examples
{: .no_toc }
Below are some use cases of the tool and the expected output.
- TOC
{:toc}

## Get a summary of the benchmark
**Command:**
```bash
python pymigbench.py summary
```
`summary` is the default query and does not accept any data type or filters. Therefore the above command is equivalent to the one below.
```bash
python pymigbench.py
```

**Result:**
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
## Get count of _lib pairs_ in `File reader/writer` domain
**Command:**
```bash
python pymigbench.py count -dt lp -f domain="File reader/writer"
```  

**Result:**
```
6 items
```
## List IDs of all _migrations_
**Command:**
```bash
python pymigbench.py list -dt mg
```

**Result:**
```yaml
157 items
- 002f5bd_flask,quart
- 0171fb9_pil,pillow
- 02b064b_pycryptodome,pycryptodomex
# (151 items hidden for brevity)
- f970b54_pil,pillow
- fe6b437_pil,pillow
- fe8e65d_dotenv,python-dotenv
157 items
```

## List IDs of _migrations_ to target library _aiohttp_
**Command:**
```bash
python pymigbench.py list -dt mg -f target=aiohttp
```

**Result:**
```yaml
11 items
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
11 items
```

## Show details of _migrations_ from _ruamel.yaml_ to _pyyaml_ in JSON format
**Command:**
```bash
python pymigbench.py detail -dt mg -f source=ruamel.yaml target=pyyaml -o json
```
**Result:**
```json
2 items
[
  {
    "id": "12e3e80_ruamel.yaml,pyyaml",
    "source": "ruamel.yaml",
    "target": "pyyaml",
    "repo": "cloud-custodian/cloud-custodian",
    "commit": "12e3e8084ddb2e7f5ccbc5ea3c3bd3e4c7e9c207",
    "pair_id": "ruamel.yaml,pyyaml",
    "commit_message": "tools/c7n_mailer - switch ruamel dependency to pyyaml (#5521)",
    "commit_url": "https://github.com/cloud-custodian/cloud-custodian/commit/12e3e808",
    "code_changes": [
      {
        "filepath": "tools/c7n_mailer/c7n_mailer/replay.py",
        "lines": [
          "25:18"
        ]
      },
      {
        "filepath": "tools/c7n_mailer/c7n_mailer/utils.py",
        "lines": [
          "28:22"
        ]
      },
      {
        "filepath": "tools/c7n_mailer/c7n_mailer/cli.py",
        "lines": [
          "15:10"
        ]
      }
    ]
  },
  {
    "id": "b955ac9_ruamel.yaml,pyyaml",
    "source": "ruamel.yaml",
    "target": "pyyaml",
    "repo": "microsoft/nni",
    "commit": "b955ac99a46094d2d701d447e9df07509767cc32",
    "pair_id": "ruamel.yaml,pyyaml",
    "commit_message": "Use PyYAML instead of ruamel.yaml (#3702)",
    "commit_url": "https://github.com/microsoft/nni/commit/b955ac99",
    "code_changes": [
      {
        "filepath": "nni/tools/nnictl/common_utils.py",
        "lines": [
          "12:12"
        ]
      },
      {
        "filepath": "test/nni_test/nnitest/utils.py",
        "lines": [
          "12:12",
          "46:46",
          "51:51"
        ]
      },
      {
        "filepath": "nni/experiment/config/common.py",
        "lines": [
          "8:8",
          "121:121"
        ]
      },
      {
        "filepath": "test/nni_test/nnitest/run_tests.py",
        "lines": [
          "12:12",
          "83:83"
        ]
      },
      {
        "filepath": "nni/experiment/config/base.py",
        "lines": [
          "9:9",
          "75:75"
        ]
      },
      {
        "filepath": "nni/tools/package_utils/__init__.py",
        "lines": [
          "9:9",
          "218:218",
          "229:229"
        ]
      }
    ]
  }
]
2 items
```