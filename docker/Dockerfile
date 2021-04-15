FROM igibson/igibson-gui:v1.0.1

VOLUME /workspace

RUN pip install --upgrade PyYAML numpngw
RUN pip install git+https://github.com/Healthcare-Robotics/assistive-gym.git
RUN pip install git+https://github.com/Zackory/bullet3.git

WORKDIR /workspace