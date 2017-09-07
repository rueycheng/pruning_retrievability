TOOLS = ../../tools
BIN = $(TOOLS)/local/bin

INDEX = full_index

METHODS = dcp infinite_renyi tcp up
RATIOS = 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
CONFIGS = $(foreach M,$(METHODS),$(foreach R,$(RATIOS),$(M)_$(R)))


.PHONY: estimates pruned_indexes results

.DELETE_ON_ERROR:


# Data (e.g. indri index, bigram queries, etc)
#
# bigrams.source:
# 	$(error Bigrams file '$@' is missing)
#
# bigrams.filtered: bigrams.source
# 	python $(TOOLS)/python/filter_bigrams.py $< > $@
#
# bigrams.dedup: bigrams.filtered
# 	sort -k1,2 $< | python $(TOOLS)/python/merge_counts.py > $@
#
# bigrams.sample_200k: bigrams.dedup
# 	python $(TOOLS)/python/weighted_sample.py $< 200000 > $@

full_index/manifest:
	$(error Indri repo '$(@D)' is missing or invalid)

docids: full_index/manifest
	$(BIN)/dump_docids full_index > $@

# Generate estimate.*
#
estimates: $(addprefix estimate.,$(METHODS))

define create-estimate-target
estimate.$(1):
	$(BIN)/IndriPruneIndex -pruneIndex -index=$(INDEX) -method=$(1) \
	    -estimate="method:reservoir,size:10000000" -rule="method:okapi" -softmax=1 > $$@
endef

$(foreach M,$(METHODS),$(eval $(call create-estimate-target,$(M))))


# Run pruning to generate pruned_indexes/*
#
pruned_indexes: $(foreach C,$(CONFIGS),pruned_indexes/$(C)/manifest)

pruned_indexes/.timestamp:
	mkdir -p $(@D)
	touch $@

define create-pruned-index-target
pruned_indexes/$(1)_$(2)/manifest: estimate.$(1) pruned_indexes/.timestamp
	$(BIN)/IndriPruneIndex -pruneIndex -index=$(INDEX) -method=$(1) \
	    -epsilon=$$(shell python $(TOOLS)/python/parse_estimate.py estimate.$(1) $(2)) \
	    -rule="method:okapi" -softmax=1 -newindex=pruned_indexes/$(1)_$(2)
endef

$(foreach M,$(METHODS),$(foreach R,$(RATIOS),$(eval $(call create-pruned-index-target,$(M),$(R)))))


# Run retrieval
#
results: $(foreach C,full_index $(CONFIGS),results/run.$(C)) \
    $(foreach C,full_index $(CONFIGS),results/eval_run.$(C))

results/.timestamp:
	mkdir -p $(@D)
	touch $@

results/run.full_index: full_index bigrams.sample_200k results/.timestamp
	python $(TOOLS)/python/compute_retrievability.py -k 100 -threads 24 -rule 'method:okapi,k1:0.9,b:0.4' \
	    bigrams.sample_200k full_index results/run.full_index results/timing.full_index

results/eval_run.full_index: full_index topics results/.timestamp
	$(BIN)/IndriRunQuery -index=full_index -count=1000 -trecFormat=1 -rule='method:okapi,k1:0.9,b:0.4' topics > $@

define create-run-target
results/run.$(1): pruned_indexes/$(1)/manifest bigrams.sample_200k results/.timestamp
	python $(TOOLS)/python/compute_retrievability.py -k 100 -threads 24 -rule 'method:okapi,k1:0.9,b:0.4' \
	    bigrams.sample_200k pruned_indexes/$(1) results/run.$(1) results/timing.$(1)
results/eval_run.$(1): pruned_indexes/$(1)/manifest topics results/.timestamp
	$(BIN)/IndriRunQuery -index=pruned_indexes/$(1) -count=1000 -trecFormat=1 -rule='method:okapi,k1:0.9,b:0.4' topics > $$@
endef

$(foreach C,$(CONFIGS),$(eval $(call create-run-target,$(C))))


# Compute retrievability
#
ret_output: $(foreach C,full_index $(CONFIGS),ret_output/ret.$(C))

ret_output/.timestamp:
	mkdir -p $(@D)
	touch $@

define script_output
[inputs]
results_file_list = $<
docid_list = docids
[outputs]
results_directory =
results_output = $(subst script,ret,$@)
show_titles = True
endef

export script_output

define create-ret-target
ret_output/list.$(1): ret_output/.timestamp
	echo results/run.$(1) > $$@
ret_output/script.$(1): ret_output/list.$(1)
	echo "$$$$script_output" > $$@
ret_output/ret.$(1): ret_output/script.$(1) docids
	python $(TOOLS)/retrievability_tools/retrievability_calculator/retrievability_calculator.py $$<
endef

$(foreach C,full_index $(CONFIGS),$(eval $(call create-ret-target,$(C))))


# Run eval topics
#
gini.table: $(foreach C,full_index $(CONFIGS),ret_output/ret.$(C))
	python $(TOOLS)/python/gini.py $^ > $@

timing.table: $(foreach C,full_index $(CONFIGS),results/timing.$(C))
	python $(TOOLS)/python/timing.py $^ > $@

eval.table: $(foreach C,full_index $(CONFIGS),results/eval_run.$(C))
	python $(TOOLS)/python/trec_eval.py qrels $^ > eval.table


# need to be in this exact order
gov2.csv: eval.table gini.table timing.table
	python $(TOOLS)/python/combine_tables.py $^ > $@
