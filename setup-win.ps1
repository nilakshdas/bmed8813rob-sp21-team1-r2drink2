# Install Chocolatey (https://chocolatey.org/install)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString("https://chocolatey.org/install.ps1"))

# Install Chocolatey packages
choco install -y cmake --installargs "ADD_CMAKE_TO_PATH=System"
choco install -y make
choco install -y git
choco install -y pyenv-win

# Install correct python version
pyenv install 3.7.7

# Install poetry
(Invoke-WebRequest -Uri "https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py" -UseBasicParsing).Content | python -