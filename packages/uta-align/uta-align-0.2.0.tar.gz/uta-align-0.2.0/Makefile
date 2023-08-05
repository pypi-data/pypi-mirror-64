# Makefile for Python project

.DELETE_ON_ERROR:
.PHONY: FORCE
.PRECIOUS:
.SUFFIXES:

SHELL:=/bin/bash -e -o pipefail
SELF:=$(firstword $(MAKEFILE_LIST))

PKG=uta_align
PKGD=$(subst .,/,${PKG})

PYV=3.7
VEDIR=venv/${PYV}


# Ignore packages in user directory (~/.local/lib/python*)
export PYTHONNOUSERSITE=1


############################################################################
#= BASIC USAGE
default: help

#=> help -- display this help message
help:
	@sbin/makefile-extract-documentation "${SELF}"


############################################################################
#= SETUP, INSTALLATION, PACKAGING

#=> devready: create venv and install pkg in develop mode
.PHONY: devready
devready:
	make ${VEDIR} && source ${VEDIR}/bin/activate && make develop
	@echo '#################################################################################'
	@echo '###  Do not forget to `source ${VEDIR}/bin/activate` to use this environment  ###'
	@echo '#################################################################################'

#=> venv: make a Python 3 virtual environment
venv/3 venv/3.5 venv/3.6 venv/3.7: venv/%:
	python$* -mvenv $@; \
	source $@/bin/activate; \
	python -m ensurepip --upgrade; \
	pip install --upgrade pip setuptools

#=> develop: install package in develop mode
develop:
	pip install -e .[dev]

#=> install: install package
#=> bdist bdist_egg bdist_wheel build sdist: distribution options
.PHONY: bdist bdist_egg bdist_wheel build build_sphinx sdist install
bdist bdist_egg bdist_wheel build sdist install: %:
	python setup.py $@


#=> upload, upload-test: upload package to pypi
.PHONY: upload upload-test
upload:
	# N.B. pypi biocommons password is in keyring
	# keyring set https://upload.pypi.org/legacy/ biocommons
	rm -fr dist
	python setup.py sdist
	twine upload -u biocommons dist/*

upload-test:
	# N.B. pypi biocommons password is in keyring
	# keyring set https://test.pypi.org/legacy/ reece
	rm -fr dist
	python setup.py sdist
	twine upload -u reece --repository-url https://test.pypi.org/legacy/ dist/*




############################################################################
#= TESTING
# see test configuration in setup.cfg

#=> test: execute tests
.PHONY: test
test:
	pytest 

#=> tox: execute tests via tox
.PHONY: tox
tox:
	tox


############################################################################
#= UTILITY TARGETS

# N.B. Although code is stored in github, I use hg and hg-git on the command line
#=> reformat: reformat code with yapf and commit
.PHONY: reformat
reformat:
	@if hg sum | grep -qL '^commit:.*modified'; then echo "Repository not clean" 1>&2; exit 1; fi
	@if hg sum | grep -qL ' applied'; then echo "Repository has applied patches" 1>&2; exit 1; fi
	yapf -i -r "${PKGD}" tests
	hg commit -m "reformatted with yapf"

#=> docs -- make sphinx docs
.PHONY: docs
docs: develop
	# RTD makes json. Build here to ensure that it works.
	make -C docs html json

############################################################################
#= CLEANUP

#=> clean: remove temporary and backup files
.PHONY: clean
clean:
	find . \( -name \*~ -o -name \*.bak \) -print0 | xargs -0r rm

#=> cleaner: remove files and directories that are easily rebuilt
.PHONY: cleaner
cleaner: clean
	rm -fr .cache *.egg-info build dist doc/_build htmlcov
	find . \( -name \*.pyc -o -name \*.orig -o -name \*.rej -o -name \*.so \) -print0 | xargs -0r rm
	find . -name __pycache__ -print0 | xargs -0r rm -fr

#=> cleanest: remove files and directories that require more time/network fetches to rebuild
.PHONY: cleanest
cleanest: cleaner
	rm -fr .eggs .tox tmp venv

#=> purge: aggresseively remove cached dependencies to force a complete rebuild
.PHONY: purge
purge: cleanest
	find ~/.cache/pip -name pysam-\* -print0 | xargs -0r rm -v



## <LICENSE>
## Copyright 2016 Source Code Committers
## 
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## 
##     http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## </LICENSE>
