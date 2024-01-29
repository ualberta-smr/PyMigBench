PyMigBench is a benchmark of Python Library Migrations. 
This repository contains the data and code for the dataset.


## PyMigBench v2
This is the latest version of the dataset.
This includes all data from [PyMigBench v1](#pymigbench-v1) and additional migrations borrowed from the [SALM dataset](https://ieeexplore.ieee.org/document/10123560).
The data also includes more information per migration-related code change.
The dataset includes 3,096 migration-related code changes from 335 migrations between 141 analogous library pairs.
The data is available in the [v2](/v2) directory.

The paper is published in FSE 2024.
We will add the citation info once it is available.
[Release 2.0.1](https://github.com/ualberta-smr/PyMigBench/releases/v2.0.1) points to the exact dataset linked to the paper.
We may update the [v2](/v2) directory to correct any mistakes or add more data and it may go out of sync with the paper.
So, for reproduction of the paper, use the release mentioned above.
For, the latest data, use the [v2](/v2) directory of the latest version of the repository.


## PyMigBench v1
The 2023 version of the dataset includes 375 migration-related code changes from 75 migrations between 34 analogous library pairs.
The data is also available in the [v1](/v1) directory.
Please visit [the PyMigBench website](https://ualberta-smr.github.io/PyMigBench) for detailed instructions on using PyMigBench v1. 
We recommend using [PyMigBench v2](#pymigbench-v2) for any new research,
however, if you are going to use this version, please cite the [MSR 2023 paper](https://ieeexplore.ieee.org/abstract/document/10174111) as below.
[Release 1.0.3](https://github.com/ualberta-smr/PyMigBench/releases/v1.0.3) points to the dataset linked to the paper.

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