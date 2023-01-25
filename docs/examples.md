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
- library pair: 59
  migration: 157
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
## List all _migrations_
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

## Find all _migrations_ to target library _aiohttp_
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
