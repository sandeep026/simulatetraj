@echo off
pip freeze > installed_packages.txt
for /F "delims==" %%i in (installed_packages.txt) do (
    echo Uninstalling %%i...
    pip uninstall -y %%i
)
del installed_packages.txt
