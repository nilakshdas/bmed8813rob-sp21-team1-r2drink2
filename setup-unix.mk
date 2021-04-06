PYENV_ROOT = $(HOME)/.pyenv
POETRY_ROOT = $(HOME)/.poetry


$(PYENV_ROOT):
	curl -sSL https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
	@echo && echo "Press any key to continue..." && read key

.PHONY: pyenv
pyenv: | $(PYENV_ROOT)
	pyenv install --skip-existing

$(POETRY_ROOT):
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

.PHONY: base_deps
base_deps: pyenv $(POETRY_ROOT) 