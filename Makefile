SPHINXOPTS  ?=
SPHINXBUILD ?= sphinx-build
SOURCEDIR   = docs
BUILDDIR    = docs/_build
HTMLDIR     = $(BUILDDIR)/html

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

gh-pages:
	ghp-import -n $(HTMLDIR)

serve:
	python -m http.server --directory docs/_build/html

dev:
	sphinx-autobuild docs docs/_build/html

%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
