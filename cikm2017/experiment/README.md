# GOV2 Experiment #

Repeat the following steps to replicate our results.

1.  Build a full index over the TREC GOV2 collection (replace `/path/to/gov2`
    with the actual path):
    ```
    IndriBuildIndex build_param -index=full_index -corpus.path=/path/to/gov2 -corpus.class=trecweb
    ```
    
    Be sure to use the the build under `tools/local/bin` to create this index.
    Or simply make a symlink at `full_index` if such index already exists
    (built under the same Indri version).
    
2.  Generate pruned indexes under various prune ratios and pruning algorithms:
    ```
    make -j2 pruned_indexes
    ```

    A horde of indexes will be created under `pruned_indexes`, which take up roughly _9 Terabytes_ of disk space.

3.  Run sample queries (`bigram.sample_200k`) to produce retrievability runs and timings.
    ```
    make results
    ```

    The results will be stored under `ret_output`.  Note that the
    retrievability runs on each index will automatically spread across multiple
    cores (24 at most), so be sure that no `-j` option is specified when
    invoking this step.

4.  Score each index with benchmark queries (TREC Topic 701-850) and compile
    all results into one CSV file `gov2.csv`.
    ```
    make -j8 gov2.csv
    ```

One can then copy the `gov2.csv` file to parent directory for further analysis.
