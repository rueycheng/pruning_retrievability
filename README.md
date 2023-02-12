#  Retrievability Experiments for Pruned Indexes

A series of analyses over the retrievability of pruned/optimized indexes is made available in this repository.  For further information regarding the scope of this research and the experimental design, consult this paper:

```
@inproceedings{chen_retrievability_2017,
 author = {Chen, Ruey-Cheng and Azzopardi, Leif and Scholer, Falk},
 title = {An Empirical Analysis of Pruning Techniques: Performance, Retrievability and Bias},
 booktitle = {Proceedings of {CIKM} '17},
 year = {2017},
 pages = {2023--2026},
 publisher = {ACM}
} 
```

## Get Started ##

Initialize submodules after cloning this repo:
```
git submodule update --init --recursive
```

Build the toolchain (replace `/path/to/boost` with actual path to Boost installation):
```
make BOOST_PREFIX=/path/to/boost -C tools
```

## Experiments ##

Data and code are available in the following directories:
* [CIKM '17 experiments](cikm2017/)
