PYENV_ROOT = $(USERPROFILE)\.pyenv
POETRY_ROOT = $(USERPROFILE)\.poetry


.PHONY: base_deps
base_deps:
	powershell -ExecutionPolicy Bypass .\setup-win.ps1