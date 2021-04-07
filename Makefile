SHELL := /bin/bash

.PHONY: all
all: ubuntu_deps

.PHONY: install
install: python_deps download_ig_dataset

include setup.mk

.PHONY: clean
clean:
	rm poetry.lock
	rm -r $$(head -n 1 .done/venv)

.PHONY: simulation
simulation:
	$(POETRY) run python -m r2drink2.env

.PHONY: entrypoint
entrypoint: simulation