# CIKM '17 - An Empirical Analysis of Pruning Techniques

This experiment is based on the TREC GOV2 data.  

* [Main results](gov2.csv) in CSV format (see below)
* [IPython Notebook for the retrievability analysis](cikm2017.ipynb)
* Experiment scripts are available in [experiment](experiment/)

## Format of the Main Results ##

Note that the CSV file `gov2.csv` has the following fields:
- Effectiveness metrics
  * NDCG@k (e.g. `n@5`, `n@10`, `n@20`)
  * Precision (e.g. `p@5`, `p@10`, `p@20`)
  * MRR and MAP (e.g. `mrr`, `map`)
- `name`: Run name
- `p_method` and `p_ratio`: Pruning algorithm and prune ratio
- `measure`: Retrievability measure e.g., `cm_10` or `gm_1.0`
- `r_sum`: Total retrievability e.g., summation of _r(d)_
- `n_docs`: Number of docs
- `gini`: Gini coefficient
- `time`: Query execution time (for running retrievability queries) 
