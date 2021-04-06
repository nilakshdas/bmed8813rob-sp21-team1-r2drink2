ifeq ($(OS),Windows_NT) 
    include setup-win.mk
else
    include setup-unix.mk
endif

.PHONY: clean_win
clean_win:
	powershell "Remove-Item -ErrorAction Ignore poetry.lock; $$null"
	powershell "Remove-Item -ErrorAction Ignore .venv; $$null"

.PHONY: clean_unix
clean_unix:
	rm -rf poetry.lock
	rm -rf .venv

poetry.lock: pyproject.toml | $(PYENV_ROOT) $(POETRY_ROOT)
	poetry lock -vvv

.venv: poetry.lock | $(PYENV_ROOT) $(POETRY_ROOT)
	poetry install -vvv
	poetry run pip install git+https://github.com/Zackory/bullet3.git
	poetry run pip install git+https://github.com/Healthcare-Robotics/assistive-gym.git
	touch $@ # update timestamp

.PHONY: python_deps
python_deps: .venv

.done/download_ig_dataset:
	poetry run python -m gibson2.utils.assets_utils --download_ig_dataset
	touch $@

.PHONY: download_ig_dataset
download_ig_dataset: .done/download_ig_dataset

.PHONY: test_imports
test_imports:
	poetry run python -m r2drink2.test