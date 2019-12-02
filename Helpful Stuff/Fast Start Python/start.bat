@echo off

mkdir NEW_PROJECT
cd NEW_PROJECT
python -m venv env
cd env
cd Scripts
call activate.bat
pause
cd ..
cd ..
cd ..
pause
pip install -r requirements.txt

pause