---
name: Query request
about: Describe this issue template's purpose here.
title: 'Query request: [short description of the query]'
labels: query request
assignees: mohayemin

---

**A one-line English description of the query.**
Ex. List all code changes having one-to-many function call replacement.
This should be the same as what you described in the issue title.

**(Optional) if the one-line description seems insufficient, describe the query further.**

**Proposed query syntax**
```bash
python pymigbench.py list -dt cc -f program_element="function call" cardinality="1-n"
```
