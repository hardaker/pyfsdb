# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

SUBMODULES    = $(patsubst %.md,%.rst,$(wildcard tools/*.md))

# build rest files from markdown
%.rst: %.md cli.template Makefile
	pandoc -i $< -o $@ > $@
	TOOL=$$(echo $$(basename $@) | sed 's/.rst//') ; \
	cat cli.template | perl -p -e "s/TOOL/$$TOOL/g" >> $@

.PHONY: help Makefile submodules

submodules: $(SUBMODULES)
	echo $(SUBMODULES)
	echo $(wildcard tools/*.md)

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html: Makefile submodules
	@PYTHONPATH=.. $(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

latex: Makefile
	@PYTHONPATH=.. $(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

latexpdf: Makefile
	@PYTHONPATH=.. $(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

clean: Makefile
	@PYTHONPATH=.. $(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
