# ----------------------------------------------------------------------
# OS dependent configuration
# ----------------------------------------------------------------------

VENV=venv/bin/
LIB=venv/Lib/site-packages/
MARKER=venv/marker
EXE=
ifeq ($(OS),Windows_NT)
VENV=venv/Scripts/
LIB=venv/Lib/site-packages/
MARKER=venv/marker
EXE=.exe
endif{%- if "True" == cookiecutter.docker %}


# ----------------------------------------------------------------------
# Docker detection
# ----------------------------------------------------------------------
ifeq ($(shell docker compose ps --services --filter "status=running"),)
DOCKER_RUNNING=false
else
DOCKER_RUNNING=true
endif{%- endif %}


# ----------------------------------------------------------------------
# Python interpreter detection
# ----------------------------------------------------------------------

ARG_COMMAND="import sys;print(sys.version_info[:2]>=(3, 8))"

ifeq (ok,$(shell test -e /dev/null 2>&1 && echo ok))
NULL_STDERR=2>/dev/null
else
NULL_STDERR=2>NUL
endif

ifndef PY

ifndef _PY
ifeq (True,$(shell py -3 -c $(ARG_COMMAND) $(NULL_STDERR)))
_PY=py -3
endif
endif

ifndef _PY
ifeq (True,$(shell python3 -c $(ARG_COMMAND) $(NULL_STDERR)))
_PY=python3
endif
endif

ifndef _PY
ifeq (True,$(shell python -c $(ARG_COMMAND) $(NULL_STDERR)))
PY=python
endif

endif

ifndef _PY
$(error Could not detect Python 3.8 or greather interpreter automatically, please use PY environment variable.)
endif

# Get original executable if venv
PY=$(shell $(_PY) -c "import os,sys;print(sys.base_prefix.replace(os.sep,'/') + ('/python.exe' if os.name == 'nt' else '/bin/python3'))")

endif

ifneq (True,$(shell $(PY) -c $(ARG_COMMAND) $(NULL_STDERR)))
$(error $(PY) is not a valid Python 3.8 or greather interpreter)
endif

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

GIT=git
PIP=$(PY) -m pip
VENV_PY=$(VENV)python$(EXE)
VENV_PIP=$(VENV)pip$(EXE)
CURRENT_DIR:=$(subst /,\,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

RM_GLOB=$(PY) -c "import shutil,sys,pathlib;[shutil.rmtree(sp, ignore_errors=False) if sp.is_dir() else sp.unlink() for p in sys.argv[1:]for sp in pathlib.Path().resolve().glob(p)]"
BROWSER=$(PY) -c "import os,webbrowser,sys;from urllib.request import pathname2url;webbrowser.open('file:'+pathname2url(os.path.abspath(sys.argv[1])))"
EXTRACT_HELP=$(PY) -c "import re,sys;m=[re.match(r'^([a-zA-Z_-]+):.*?\#\# (.*)$$',line)for line in sys.stdin];print('\n'.join('{:14} {}'.format(*g.groups())for g in m if g))"
LS=$(PY) -c "import sys,os;print('\n'.join(os.listdir(os.path.abspath(sys.argv[1]))))"
TOUCH=$(PY) -c "import sys;open(sys.argv[1],'xb')"

TOX=$(VENV)tox$(EXE)
SPHINX=$(VENV)sphinx-build$(EXE)
COVERAGE=$(VENV)coverage$(EXE)
TWINE=$(VENV)twine$(EXE)
PRECOMMIT=$(VENV)pre-commit$(EXE)


# ----------------------------------------------------------------------
# Automatic installation
# ----------------------------------------------------------------------

.git:
	$(GIT) init
	$(GIT) add * .editorconfig .gitignore .github/ .pre-commit-config.yaml
	$(GIT) commit -m "Initial commit"
	$(GIT) branch -M main
	$(GIT) remote add origin {{ cookiecutter.__clone_url }}

# We need to resolve virtualenv : it can be missing or installed with pip or apt
ifneq (,$(shell $(PIP) show virtualenv $(NULL_STDERR)))
.PHONY: vritalenv
virtualenv:
	$(PIP) show virtualenv
	$(PY) -m virtualenv venv
else
ifneq (,$(shell virtualenv --version))
.PHONY: vritalenv
virtualenv:
	virtualenv --version
	virtualenv venv
else
.PHONY: vritalenv
virtualenv:
	$(PIP) install virtualenv
	$(PIP) show virtualenv
	$(PY) -m virtualenv venv
endif
endif

$(MARKER):
	$(PY) --version
	$(PIP) --version
	$(MAKE) clean
	$(MAKE) .git
	$(MAKE) virtualenv
	$(VENV_PIP) install 'setuptools>=62.0.0' 'pip>=21.3'
	$(VENV_PIP) install -e .[pre-commit,lint]
ifeq ($(USE_FORMATER),)
	$(PRECOMMIT) install
endif
	$(TOUCH) $(MARKER)

$(VENV): $(MARKER)

$(VENV_PY): $(MARKER)

$(VENV_PIP): $(MARKER)

$(TOX): $(VENV_PIP)
	$(VENV_PIP) install -e .[tox]

$(PRECOMMIT): $(VENV_PIP)

$(SPHINX): $(VENV_PIP)
	$(VENV_PIP) install -e .[docs]

$(COVERAGE): $(VENV_PIP)
	$(VENV_PIP) install -e .[cov]

$(TWINE): $(VENV_PIP)
	$(VENV_PIP) install -e .[deploy]

$(LIB)build: $(VENV_PIP)
	$(VENV_PIP) install -e .[build]


# ----------------------------------------------------------------------
# Commands
# ----------------------------------------------------------------------

.DEFAULT_GOAL := help

.PHONY: clean
clean:  ## Remove all build, test, coverage, venv and Python artifacts.
ifeq ($(OS),Windows_NT)
	PowerShell "Get-Process | Where-Object {$$_.path -like '$(CURRENT_DIR)venv\Scripts\*'} | Stop-Process -Force"
endif
	$(RM_GLOB) 'venv/*/python.?e?x?e?' 'venv' 'build/' 'dist/' 'public/' '.eggs/' '.tox/' '.coverage' 'htmlcov/' '.pytest_cache' '.mypy_cache' '.ruff_cache'  '**/*.egg-info' '**/*.egg' '**/__pycache__' '**/*~' '**/*.pyc' '**/*.pyo'

.PHONY: cov
cov: $(TOX)  ## Check code coverage.
	$(TOX) -e cov

.PHONY: dist
dist: clean $(LIB)build  ## Builds source and wheel package.
	$(VENV_PY) -m build
	$(LS) dist/{%- if "True" == cookiecutter.docker %}

.PHONY: docker-logs
docker-logs:  ## Check and follow docker logs.
	docker compose logs -f

.PHONY: docker-up
docker-up:  ## Run docker as deamon and rebuild image.
	docker compose up -d --build --force-recreate

.PHONY: docker-stop
docker-stop:  ## Stop all containers.
	docker compose stop

.PHONY: docker-down
docker-purge:  ## Remove and drop every image, container and network.
	docker compose down --volumes --rmi 'all'

ifeq ($(DOCKER_RUNNING),true)
.PHONY: docker-restore
docker-restore:  ## Restore logs backup.
	docker compose stop
	docker run --rm \
		-v "{{ cookiecutter.__project_slug }}_logs:/logs" \
		-v "$$PWD":/backup \
		ubuntu \
		bash -c "cd / && rm -rf /{logs}/* && tar xvfP /backup/backup.tar.gz"
	docker compose up -d

.PHONY: docker-backup
docker-backup:  ## Make backups of logs.
	docker compose stop
	docker run --rm \
		-v "{{ cookiecutter.__project_slug }}_logs:/logs" \
		-v "$$PWD":/backup \
		ubuntu \
		tar czvf /backup/backup.tar.gz -C / logs
	docker compose up -d

.PHONY: docker-shell
docker-shell:	## Get a shell in the running container.
	docker compose run {{ cookiecutter.__project_slug }} bash
else
.PHONY: docker-restore
docker-restore:
	docker run --rm \
		-v "{{ cookiecutter.__project_slug }}_logs:/logs" \
		-v "$$PWD":/backup \
		ubuntu \
		bash -c "cd / && rm -rf /{logs}/* && tar xvfP /backup/backup.tar.gz"

.PHONY: docker-backup
docker-backup:
	docker run --rm \
		-v "{{ cookiecutter.__project_slug }}_logs:/logs" \
		-v "$$PWD":/backup \
		ubuntu \
		tar czvf /backup/backup.tar.gz -C / logs

.PHONY: docker-shell
docker-shell:
	docker compose exec {{ cookiecutter.__project_slug }} /bin/bash
endif{%- endif %}

.PHONY: docs
docs: $(SPHINX) ## Generate Sphinx HTML documentation.
	$(SPHINX) -W -b html docs public

.PHONY: format
format: $(PRECOMMIT)  ## Format style with pre-commit, ruff, black and mypy.
	$(PRECOMMIT) run --all-files

.PHONY: help
help:  ## Show current message.
	@$(EXTRACT_HELP) < $(MAKEFILE_LIST)

.PHONY: install
install:  ## Install the package to the active Python's site-packages.
	$(PIP) install .

.PHONY: lint
lint: $(TOX)  ## Check style with tox, ruff, black and mypy.
	$(TOX) -e lint

.PHONY: open-docs
open-docs: docs  ## Open documentation.
	$(BROWSER) public/index.html

.PHONY: open-cov
open-cov: cov  ## Open coverage report.
	$(BROWSER) htmlcov/index.html

.PHONY: release
release: dist $(TWINE)  ## Package and upload a release.
	$(TWINE) upload dist/*

.PHONY: setup
setup: clean $(VENV_PY)  ## Create virtual environment and install pre-commit.

.PHONY: tests
tests: $(TOX)  ## Run unit and functional tests.
	$(TOX) -e tests

.PHONY: tests-all
tests-all: $(TOX)  ## Run all tests in parallel (docs, lint and tests).
	$(TOX)

.PHONY: uninstall
uninstall:  ## Install the package to the active Python's site-packages.
	$(PIP) uninstall {{ cookiecutter.__project_slug }}
