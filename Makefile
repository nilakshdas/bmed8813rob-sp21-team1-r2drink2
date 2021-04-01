.PHONY: python_deps
python_deps:
	pip install --upgrade PyYAML
	pip install gibson2 numpngw
	pip install git+https://github.com/Healthcare-Robotics/assistive-gym.git
	pip install git+https://github.com/Zackory/bullet3.git
	yes | python -m gibson2.utils.assets_utils --download_ig_dataset