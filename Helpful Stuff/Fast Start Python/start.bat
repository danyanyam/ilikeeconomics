@echo off

mkdir NEW_PROJECT
cd NEW_PROJECT
python -m venv env
cd env
cd Scripts
call activate.bat
cd ..
cd ..
cd ..
python -m pip install --upgrade pip
pip install -r requirements.txt

pause
