HERE = $(shell pwd)

VENV_CMD    := python3 -m venv
VENV_DIR    := $(HERE)/.venv
PYTHON      := $(VENV_DIR)/bin/python
PYTEST      := $(VENV_DIR)/bin/pytest
PYFLAKES    := $(VENV_DIR)/bin/pyflakes
PYBLACK     := $(VENV_DIR)/bin/black

BUILD_DIRS = bin .build build include lib lib64 man share package *.egg

DRY ?= true
ifneq ($(DRY),false)
  PYBLACK_OPTS := --diff --check
endif

.PHONY: build
build: $(VENV_DIR)
	$(PYTHON) -m build

.PHONY: clean
clean: $(VENV_DIR)
	find tornado_rest_client -type f -name '*.pyc' -exec rm "{}" \;
	rm -rf $(BUILD_DIRS)
	PATH=$(VENV_DIR)/bin:$(PATH) $(MAKE) -C docs clean

.PHONY: lint
lint: $(VENV_DIR)
	$(PYBLACK) $(PYBLACK_OPTS) tornado_rest_client

.PHONY: test
test: $(VENV_DIR)
	PYTHONPATH=$(HERE) $(PYTEST) --cov=tornado_rest_client -v
	PYTHONPATH=$(HERE) $(PYFLAKES) tornado_rest_client

.PHONY: docs
docs: $(VENV_DIR)
	PATH=$(VENV_DIR)/bin:$(PATH) $(MAKE) -C docs html

.PHONY: venv
venv: $(VENV_DIR)

$(VENV_DIR): requirements.txt requirements.test.txt
	$(VENV_CMD) $(VENV_DIR)
	$(PYTHON) -m pip install -U pip setuptools wheel
	$(PYTHON) -m pip install -r requirements.test.txt
	$(PYTHON) -m pip install -r requirements.txt
	touch $(VENV_DIR)
