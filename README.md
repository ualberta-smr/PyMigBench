PyMigBench is a benchmark of Python Library Migrations. 
This repository contains the data and code for the dataset.


## PyMigBench v2
This is the latest version of the dataset.
This includes all data from [PyMigBench v1](#pymigbench-v1) and additional migrations borrowed from the [SALM dataset](https://ieeexplore.ieee.org/document/10123560).
The data also includes more information per migration-related code change.
The dataset includes 3,096 migration-related code changes from 335 migrations between 141 analogous library pairs.
The data and relevant code can be found in the [v2](/v2) directory of this repository.
The paper is published published in FSE 2023.
We will update the citation information once available.

## PyMigBench v1
The 2023 version of the dataset includes 375 migration-related code changes from 75 migrations between 34 analogous library pairs.
The data is also available in the [v1](/v1) directory.
Please visit [the PyMigBench website](https://ualberta-smr.github.io/PyMigBench) for detailed instructions on using PyMigBench v1. 
We recommend using [PyMigBench v2](#pymigbench-v2) for any new research,
however, if you are going to use this version, please cite the [MSR 2023 paper](https://ieeexplore.ieee.org/abstract/document/10174111):

```
@INPROCEEDINGS{pymigbench,
  author={Islam, Mohayeminul and Jha, Ajay Kumar and Nadi, Sarah and Akhmetov, Ildar},
  booktitle={2023 IEEE/ACM 20th International Conference on Mining Software Repositories (MSR)}, 
  title={PyMigBench: A Benchmark for Python Library Migration}, 
  year={2023},
  volume={},
  number={},
  pages={511-515},
  doi={10.1109/MSR59073.2023.00075}
}
```


## Contributors
- [Mohayeminul Islam](https://mohayemin.github.io/)
- [Ajay Kumar Jha](https://hifromajay.github.io/)
- [Sarah Nadi](https://sarahnadi.org/)
- [Ildar Akhmetov](https://ildarakhmetov.com/)  

For any queries, please contact mohayemin@ualberta.ca.