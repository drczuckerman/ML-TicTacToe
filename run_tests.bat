@echo off
set PYTHONPATH=src
python -m unittest discover test
set PYTHONPATH=
