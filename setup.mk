define append_if_not_present
    if ! grep -Fxq $(2) $(1); then echo $(2) >> $(1); fi
endef


#################### APT packages ####################

APT_PKG := .done/apt

$(APT_PKG):
	mkdir -p $@

APT_PACKAGES := \
	$(APT_PKG)/build-essential \
	$(APT_PKG)/cmake \
	$(APT_PKG)/curl \
	$(APT_PKG)/git \
	$(APT_PKG)/libbz2-dev \
	$(APT_PKG)/libffi-dev \
	$(APT_PKG)/liblzma-dev \
	$(APT_PKG)/libncurses5-dev \
	$(APT_PKG)/libncursesw5-dev \
	$(APT_PKG)/libreadline-dev \
	$(APT_PKG)/libsqlite3-dev \
	$(APT_PKG)/libssl-dev \
	$(APT_PKG)/llvm \
	$(APT_PKG)/python-openssl \
	$(APT_PKG)/python3.7 \
	$(APT_PKG)/python3-apt \
	$(APT_PKG)/python3-distutils \
	$(APT_PKG)/tk-dev \
	$(APT_PKG)/wget \
	$(APT_PKG)/xz-utils \
	$(APT_PKG)/zlib1g-dev

.PHONY: apt_update
apt_update:
	sudo apt-get -y update
	sudo apt-get -y upgrade

$(APT_PKG)/.update: | $(APT_PKG)
	$(MAKE) apt_update | tee $@; test $${PIPESTATUS[0]} -eq 0

.DELETE_ON_ERROR: $(APT_PACKAGES)
$(APT_PACKAGES): $(APT_PKG)/.update
	sudo apt-get install -y $(@F) | tee $@; test $${PIPESTATUS[0]} -eq 0

.PHONY: apt_packages
apt_packages: $(APT_PACKAGES)


#################### pyenv ####################

PYENV = $(HOME)/.pyenv/bin/pyenv

$(PYENV): | $(APT_PACKAGES)
	curl -sSL https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
	$(call append_if_not_present,$(HOME)/.bashrc,'export PATH="$$HOME/.pyenv/bin:$$PATH"')
	$(call append_if_not_present,$(HOME)/.bashrc,'eval "$$(pyenv init -)"')
	$(call append_if_not_present,$(HOME)/.bashrc,'eval "$$(pyenv virtualenv-init -)"')

.DELETE_ON_ERROR: .done/pyenv
.done/pyenv: | $(PYENV)
	$(PYENV) install --skip-existing | tee $@; test $${PIPESTATUS[0]} -eq 0

.PHONY: pyenv
pyenv: .done/pyenv


#################### poetry ####################

POETRY = $(HOME)/.poetry/bin/poetry

$(POETRY): | $(APT_PACKAGES)
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | $(PYENV) exec python -
	$(call append_if_not_present,$(HOME)/.bashrc,'export PATH="$$HOME/.poetry/bin:$$PATH"')

.DELETE_ON_ERROR: .done/poetry
.done/poetry:
	$(MAKE) $(POETRY) | tee $@; test $${PIPESTATUS[0]} -eq 0

.PHONY: poetry
poetry: .done/poetry


#################### ubuntu dependencies ####################

.PHONY: ubuntu_deps
ubuntu_deps: apt_packages pyenv poetry


#################### python dependencies ####################

poetry.lock: pyproject.toml | $(POETRY)
	$(POETRY) lock -vvv

.done/venv: poetry.lock
	$(POETRY) install -vvv
	$(POETRY) run pip install git+https://github.com/Zackory/bullet3.git
	$(POETRY) run pip install git+https://github.com/Healthcare-Robotics/assistive-gym.git
	$(POETRY) env info --path > $@

.PHONY: python_deps
python_deps: .done/venv


#################### iGibson ####################

.done/download_ig_dataset: | .done/venv
	yes | $(POETRY) run python -m gibson2.utils.assets_utils --download_ig_dataset
	touch $@

.PHONY: download_ig_dataset
download_ig_dataset: .done/download_ig_dataset