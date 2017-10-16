@echo off
set OLD_PYTHONPATH=%PYTHONPATH%
set PYTHONPATH=src
python -m unittest discover test
set PYTHONPATH=%OLD_PYTHONPATH%
set OLD_PYTHONPATH=
