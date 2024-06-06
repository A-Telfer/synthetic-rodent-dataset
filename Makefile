#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = synthetic_rodents
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python
BLENDER = /home/andretelfer/blender-3.4.1-linux-x64/blender

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python Dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt


## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 synthetic_rodents
	black --check --config pyproject.toml synthetic_rodents


## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml synthetic_rodents


## Render the 20240530 dataset 
.PHONY: render-demo-20240530
render-demo-20240530: requirements
	$(BLENDER) data/blender/demo_20240530.blend --background --python synthetic_rodents/data/demo_20240530/make_dataset.py
	$(PYTHON_INTERPRETER) synthetic_rodents/data/demo_20240530/visualize.py
	echo "Demo dataset rendered and visualized data/tests/demo_20240530"


## Make Demo Dataset
.PHONY: extract-real-frames
extract-real-frames: requirements
	$(PYTHON_INTERPRETER) synthetic_rodents/extract_frames.py
	


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z0-9_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)