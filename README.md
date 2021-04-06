# R2Drink2


## Windows setup

1. Disable Microsoft Store for running python.

> **Settings** > **Manage App Execution Aliases** > *uncheck all options with "python.exe"*

2. Install Microsoft Visual C++ 14.0:
https://yugdamor.medium.com/microsoft-visual-c-14-0-724d91d00590


Now, in PowerShell (run as administrator), execute the following commands one at a time:

```powershell
cd path\to\bmed8813rob-sp21-team1-r2drink2
Set-ExecutionPolicy -Scope Process -Force -ExecutionPolicy Bypass; .\setup-win.ps1

# ~~~ RESTART POWERSHELL ~~~ #

make python_deps
make download_ig_dataset
```
