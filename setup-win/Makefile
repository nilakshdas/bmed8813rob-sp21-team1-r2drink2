JQ = jq --indent 4 -r
PYENV_ROOT = $(HOME)/.pyenv
PYENV = $(HOME)/.pyenv/bin/pyenv

RANDOM := $(shell python -c "import random; print(int(random.random() * 10000))")


.PHONY: clean_python
clean_python:
	rm -rfv **/__pycache__
	rm -rfv **/.ipynb_checkpoints

.PHONY: clean
clean: clean_python

$(PYENV_ROOT):
	curl -sSL https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
	@echo && echo "Press any key to continue..." && read key