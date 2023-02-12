BOOST_PREFIX = $(error Re-run with "make BOOST_PREFIX=/path/to/boost")
LOCAL = $(abspath local)
INDRI_BUILD = indri-5.9


.PHONY: all

.DELETE_ON_ERROR:

all: $(LOCAL)/bin/IndriRunQuery $(LOCAL)/bin/IndriPruneIndex $(LOCAL)/bin/dump_docids


# IndriRunQuery
#
indri-pruning-toolkit/share/DocListMemoryBuilder.patch:
	$(error Run "git submodule update --init --recursive" from repo root and try again)

$(INDRI_BUILD).tar.gz:
	wget https://sourceforge.net/projects/lemur/files/lemur/$(INDRI_BUILD)/$(INDRI_BUILD).tar.gz/download -O $@

$(INDRI_BUILD)/.patched: $(INDRI_BUILD).tar.gz indri-pruning-toolkit/share/DocListMemoryBuilder.patch
	tar zxvf $<
	cd $(@D) && patch -p1 < ../indri-pruning-toolkit/share/DocListMemoryBuilder.patch
	cd $(@D) && sh ./configure --prefix=$(LOCAL)
	touch $@

$(LOCAL)/bin/IndriRunQuery $(LOCAL)/share/indri/Makefile.app: $(INDRI_BUILD)/.patched 
	make -j8 -C $(<D)
	make -C $(<D) install


# IndriPruneIndex
#
indri-pruning-toolkit/config.status: indri-pruning-toolkit/configure
	cd $(@D) && sh ./configure --prefix=$(LOCAL) --with-indri=$(LOCAL) --with-boost=$(BOOST_PREFIX)

$(LOCAL)/bin/IndriPruneIndex: indri-pruning-toolkit/config.status
	make -C $(<D)
	make -C $(<D) install


# dump_docids
#
dump_docids/Makefile: $(LOCAL)/share/indri/Makefile.app
	perl -pe's/(?<=APP=)/dump_docids/' $< > $@

dump_docids/dump_docids: dump_docids/Makefile dump_docids/dump_docids.cpp
	make -C $(<D)

$(LOCAL)/bin/dump_docids: dump_docids/dump_docids
	cp $< $@

