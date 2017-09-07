#  Retrievability Experiments for Pruned Indexes

A series of analyses over the retrievability of pruned/optimized indexes is made available in this repository.  For further information regarding the scope of this research and the experimental design, consult this paper:

> Ruey-Cheng Chen, Leif Azzopardi, and Falk Scholer. 2017. An Empirical Analysis of Pruning Techniques. In Proceedings of CIKM '17, to appear.

If you use the code in your research project, please cite the paper.

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
